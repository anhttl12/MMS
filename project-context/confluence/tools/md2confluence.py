#!/usr/bin/env python3
"""md2confluence — chuyển Markdown (GFM) sang Confluence Storage Format (XHTML).

Hỗ trợ: heading, đoạn văn, bảng GFM (kể cả <br/> trong ô), code fence -> code macro,
mermaid fence -> ảnh attachment, danh sách lồng nhau, blockquote -> panel/info,
hr, inline **bold** *italic* `code` [link](url).

Dùng:  python3 md2confluence.py <file.md ...> --out DIR [--images-dir DIR] [--toc] [--mermaid-format png]
"""
import argparse
import os
import re
import sys

# ---------------------------------------------------------------- inline

ALLOWED_INLINE_HTML = re.compile(r'<br\s*/?>', re.I)
CODE_SPAN = re.compile(r'(``+)(.+?)\1|`([^`\n]+)`')
BOLD = re.compile(r'\*\*(?!\s)(.+?)(?<!\s)\*\*', re.S)
# Loại '<' khỏi nội dung: chặn match cắt ngang <strong> do BOLD sinh trước
# (bảo đảm XHTML well-formed; đánh đổi: *nghiêng chứa **đậm** * sẽ không thành nghiêng)
ITALIC = re.compile(r'(?<![\w*])\*(?!\s)([^*\n<]+?)(?<!\s)\*(?![\w*])')
STRIKE = re.compile(r'~~(?!\s)(.+?)(?<!\s)~~', re.S)
LINK = re.compile(r'!?\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')

PH = '\x00{}\x01'  # placeholder không xuất hiện trong markdown


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def esc_attr(text):
    return esc(text).replace('"', '&quot;')


def inline(text):
    """Chuyển inline markdown -> XHTML an toàn cho Confluence."""
    slots = []

    def stash(html):
        slots.append(html)
        return PH.format(len(slots) - 1)

    # 1. giữ lại <br/> (thẻ HTML duy nhất được phép trong nguồn)
    text = ALLOWED_INLINE_HTML.sub(lambda m: stash('<br/>'), text)

    # 2. code span: nội dung escape nguyên văn, không xử lý markdown bên trong
    def code_span(m):
        body = m.group(2) if m.group(2) is not None else m.group(3)
        return stash('<code>' + esc(body.strip() if m.group(2) else body) + '</code>')

    text = CODE_SPAN.sub(code_span, text)

    # 3. link (giữ trước khi escape để không mất dấu ngoặc)
    def link(m):
        label, href = m.group(1), m.group(2)
        if m.group(0).startswith('!'):
            return stash('<ac:image><ri:attachment ri:filename="%s" /></ac:image>'
                         % esc_attr(os.path.basename(href)))
        return stash('<a href="%s">%s</a>' % (esc_attr(href), esc(label) or esc_attr(href)))

    text = LINK.sub(link, text)

    # 4. escape phần còn lại
    text = esc(text)

    # 5. nhấn mạnh
    text = BOLD.sub(lambda m: '<strong>%s</strong>' % m.group(1), text)
    text = STRIKE.sub(lambda m: '<span style="text-decoration: line-through;">%s</span>' % m.group(1), text)
    text = ITALIC.sub(lambda m: '<em>%s</em>' % m.group(1), text)

    # 6. trả placeholder về
    for i, html in enumerate(slots):
        text = text.replace(PH.format(i), html)
    return text


# ---------------------------------------------------------------- code macro

# Ngôn ngữ mà macro Code của Confluence nhận; còn lại quy về "none".
CONFLUENCE_LANGS = {
    'actionscript3', 'applescript', 'bash', 'c', 'c#', 'c++', 'coldfusion', 'cpp',
    'csharp', 'css', 'cuda', 'delphi', 'diff', 'erlang', 'go', 'graphql', 'groovy',
    'haskell', 'html', 'java', 'javafx', 'javascript', 'json', 'jsx', 'kotlin',
    'less', 'lua', 'mathematica', 'objectivec', 'ocaml', 'perl', 'php', 'powershell',
    'puppet', 'python', 'r', 'ruby', 'rust', 'sass', 'scala', 'scheme', 'shell',
    'sql', 'swift', 'tex', 'text', 'typescript', 'vb', 'vbnet', 'xml', 'yaml', 'none',
}
LANG_ALIAS = {
    'js': 'javascript', 'ts': 'typescript', 'py': 'python', 'sh': 'bash', 'zsh': 'bash',
    'shell': 'bash', 'yml': 'yaml', 'jsonc': 'json', 'http': 'none', 'text': 'none',
    'txt': 'none', 'plaintext': 'none', 'console': 'bash', 'tsql': 'sql', 'psql': 'sql',
    'mermaid': 'none', 'md': 'none', 'markdown': 'none', 'ini': 'none', 'conf': 'none',
    'dockerfile': 'bash', 'proto': 'none', 'csv': 'none',
}


def cdata(body):
    # ']]>' không thể nằm trong một khối CDATA -> cắt làm hai
    return '<![CDATA[' + body.replace(']]>', ']]]]><![CDATA[>') + ']]>'


def code_macro(body, lang='', title='', collapse=False):
    lang = LANG_ALIAS.get(lang.lower(), lang.lower())
    if lang not in CONFLUENCE_LANGS:
        lang = 'none'
    p = ['<ac:parameter ac:name="language">%s</ac:parameter>' % lang]
    if title:
        p.append('<ac:parameter ac:name="title">%s</ac:parameter>' % esc(title))
    if collapse:
        p.append('<ac:parameter ac:name="collapse">true</ac:parameter>')
    return ('<ac:structured-macro ac:name="code" ac:schema-version="1">'
            + ''.join(p)
            + '<ac:plain-text-body>' + cdata(body) + '</ac:plain-text-body>'
            + '</ac:structured-macro>')


# ---------------------------------------------------------------- block parser

FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})\s*([A-Za-z0-9_+-]*)\s*$')
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
TOC_ANCHOR = re.compile(r'^<a id="muc-[^"]*"></a>$')
HR = re.compile(r'^\s{0,3}(?:-\s*-\s*-[-\s]*|\*\s*\*\s*\*[*\s]*|_\s*_\s*_[_\s]*)$')
TABLE_DELIM = re.compile(r'^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$')
BULLET = re.compile(r'^(\s*)([-*+])\s+(.*)$')
ORDERED = re.compile(r'^(\s*)(\d{1,9})[.)]\s+(.*)$')
QUOTE = re.compile(r'^\s{0,3}>\s?(.*)$')
ALIGN = {'left': 'left', 'center': 'center', 'right': 'right'}


class Converter:
    def __init__(self, doc_slug, images_dir, mermaid_ext='png', mermaid_source=False):
        self.doc_slug = doc_slug
        self.images_dir = images_dir
        self.mermaid_ext = mermaid_ext
        self.mermaid_source = mermaid_source
        self.diagrams = []  # (filename, source)

    # -- helpers ---------------------------------------------------
    def _mermaid(self, source):
        n = len(self.diagrams) + 1
        fname = '%s-diagram-%02d.%s' % (self.doc_slug, n, self.mermaid_ext)
        self.diagrams.append((fname, source))
        img = ('<p><ac:image ac:align="center" ac:layout="center">'
               '<ri:attachment ri:filename="%s" /></ac:image></p>' % esc_attr(fname))
        if self.mermaid_source:
            img += ('<ac:structured-macro ac:name="expand" ac:schema-version="1">'
                    '<ac:parameter ac:name="title">Nguồn sơ đồ (mermaid)</ac:parameter>'
                    '<ac:rich-text-body>' + code_macro(source, 'none') + '</ac:rich-text-body>'
                    '</ac:structured-macro>')
        return img

    @staticmethod
    def _split_row(line):
        line = line.strip()
        if line.startswith('|'):
            line = line[1:]
        if line.endswith('|') and not line.endswith('\\|'):
            line = line[:-1]
        cells, buf, i = [], '', 0
        while i < len(line):
            c = line[i]
            if c == '\\' and i + 1 < len(line) and line[i + 1] == '|':
                buf += '|'
                i += 2
                continue
            if c == '|':
                cells.append(buf.strip())
                buf = ''
            else:
                buf += c
            i += 1
        cells.append(buf.strip())
        return cells

    # -- main loop -------------------------------------------------
    def convert(self, text):
        text = text.replace('\r\n', '\n').replace('\r', '\n').replace('\t', '    ')
        # bỏ mục lục Markdown và thẻ neo <a id="muc-..."></a> — Confluence dùng --toc
        text = re.sub(r'<!-- TOC -->.*?<!-- /TOC -->\n?', '', text, flags=re.S)
        lines = [l for l in text.split('\n') if not TOC_ANCHOR.match(l)]
        out, i = [], 0
        while i < len(lines):
            line = lines[i]

            if not line.strip():
                i += 1
                continue

            m = FENCE.match(line)
            if m:
                marker, lang = m.group(2), m.group(3)
                body, i = [], i + 1
                close = re.compile(r'^\s*' + marker[0] + '{%d,}\\s*$' % len(marker))
                while i < len(lines) and not close.match(lines[i]):
                    body.append(lines[i])
                    i += 1
                i += 1  # bỏ dòng đóng fence
                src = '\n'.join(body).rstrip()
                if lang.lower() == 'mermaid':
                    out.append(self._mermaid(src))
                else:
                    out.append(code_macro(src, lang))
                continue

            m = HEADING.match(line)
            if m:
                lvl = len(m.group(1))
                out.append('<h%d>%s</h%d>' % (lvl, inline(m.group(2)), lvl))
                i += 1
                continue

            if HR.match(line):
                out.append('<hr />')
                i += 1
                continue

            # bảng: dòng header + dòng phân cách
            if '|' in line and i + 1 < len(lines) and TABLE_DELIM.match(lines[i + 1]) \
                    and '|' in lines[i + 1]:
                html, i = self._table(lines, i)
                out.append(html)
                continue

            if QUOTE.match(line):
                html, i = self._quote(lines, i)
                out.append(html)
                continue

            if BULLET.match(line) or ORDERED.match(line):
                html, i = self._list(lines, i)
                out.append(html)
                continue

            html, i = self._paragraph(lines, i)
            out.append(html)
        return '\n'.join(out)

    # -- bảng ------------------------------------------------------
    def _table(self, lines, i):
        header = self._split_row(lines[i])
        aligns = []
        for spec in self._split_row(lines[i + 1]):
            spec = spec.strip()
            if spec.startswith(':') and spec.endswith(':'):
                aligns.append('center')
            elif spec.endswith(':'):
                aligns.append('right')
            elif spec.startswith(':'):
                aligns.append('left')
            else:
                aligns.append('')
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip() and '|' in lines[i] \
                and not FENCE.match(lines[i]) and not HEADING.match(lines[i]) \
                and not HR.match(lines[i]):
            rows.append(self._split_row(lines[i]))
            i += 1

        ncol = max([len(header)] + [len(r) for r in rows]) if rows else len(header)

        def cell(tag, value, idx):
            style = ''
            if idx < len(aligns) and aligns[idx]:
                style = ' style="text-align: %s;"' % aligns[idx]
            return '<%s%s>%s</%s>' % (tag, style, inline(value) or '&#160;', tag)

        parts = ['<table><colgroup>' + '<col />' * ncol + '</colgroup><tbody>']
        parts.append('<tr>' + ''.join(
            cell('th', header[c] if c < len(header) else '', c) for c in range(ncol)) + '</tr>')
        for r in rows:
            parts.append('<tr>' + ''.join(
                cell('td', r[c] if c < len(r) else '', c) for c in range(ncol)) + '</tr>')
        parts.append('</tbody></table>')
        return ''.join(parts), i

    # -- blockquote ------------------------------------------------
    def _quote(self, lines, i):
        inner = []
        while i < len(lines):
            m = QUOTE.match(lines[i])
            if m:
                inner.append(m.group(1))
                i += 1
            elif lines[i].strip() and inner and not FENCE.match(lines[i]) \
                    and not HEADING.match(lines[i]) and not HR.match(lines[i]) \
                    and not BULLET.match(lines[i]) and not ORDERED.match(lines[i]):
                inner.append(lines[i])  # lazy continuation
                i += 1
            else:
                break
        body = Converter(self.doc_slug, self.images_dir, self.mermaid_ext,
                         self.mermaid_source)
        body.diagrams = self.diagrams
        html = body.convert('\n'.join(inner))
        return ('<ac:structured-macro ac:name="info" ac:schema-version="1">'
                '<ac:rich-text-body>' + html + '</ac:rich-text-body>'
                '</ac:structured-macro>'), i

    # -- danh sách -------------------------------------------------
    def _list(self, lines, i):
        items, i = self._collect_items(lines, i)
        return self._render_list(items), i

    def _collect_items(self, lines, i):
        """Thu các item cùng cấp (và con của chúng) thành cây."""
        base = None
        items = []
        while i < len(lines):
            line = lines[i]
            mb, mo = BULLET.match(line), ORDERED.match(line)
            if not (mb or mo):
                if not line.strip():
                    # dòng trống: chỉ tiếp tục nếu dòng sau vẫn thuộc danh sách
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and (BULLET.match(lines[j]) or ORDERED.match(lines[j])
                                           or (base is not None
                                               and len(lines[j]) - len(lines[j].lstrip()) > base)):
                        i = j
                        continue
                    break
                if items and base is not None and len(line) - len(line.lstrip()) > base:
                    items[-1]['cont'].append(line.strip())  # dòng nối tiếp
                    i += 1
                    continue
                break

            m = mb or mo
            indent = len(m.group(1))
            if base is None:
                base = indent
                ordered = bool(mo)
            if indent < base:
                break
            if indent > base:
                child, i = self._collect_items(lines, i)
                if items:
                    items[-1]['children'].append(child)
                continue
            if bool(mo) != ordered:
                break
            items.append({'text': m.group(3), 'cont': [], 'children': [],
                          'start': int(mo.group(2)) if mo else None})
            i += 1
        return {'ordered': ordered if items else False, 'items': items,
                'start': items[0]['start'] if items and items[0]['start'] is not None else None}, i

    def _render_list(self, node):
        if not node['items']:
            return ''
        tag = 'ol' if node['ordered'] else 'ul'
        open_tag = '<%s>' % tag
        if node['ordered'] and node['start'] not in (None, 1):
            open_tag = '<ol start="%d">' % node['start']
        parts = [open_tag]
        for it in node['items']:
            body = inline(' '.join([it['text']] + it['cont']).strip())
            parts.append('<li><p>%s</p>%s</li>' % (
                body, ''.join(self._render_list(c) for c in it['children'])))
        parts.append('</%s>' % tag)
        return ''.join(parts)

    # -- đoạn văn --------------------------------------------------
    def _paragraph(self, lines, i):
        buf = []
        while i < len(lines) and lines[i].strip():
            line = lines[i]
            if FENCE.match(line) or HEADING.match(line) or HR.match(line) \
                    or QUOTE.match(line) or BULLET.match(line) or ORDERED.match(line):
                break
            if '|' in line and i + 1 < len(lines) and TABLE_DELIM.match(lines[i + 1]) \
                    and '|' in lines[i + 1]:
                break
            buf.append(line.strip())
            i += 1
        text = '<br/>'.join(inline(b) for b in buf) if len(buf) > 1 else inline(buf[0])
        return '<p>%s</p>' % text, i


# ---------------------------------------------------------------- driver

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+')
    ap.add_argument('--out', required=True)
    ap.add_argument('--toc', action='store_true', help='chèn macro Table of Contents đầu trang')
    ap.add_argument('--mermaid-format', default='png', choices=['png', 'svg'])
    ap.add_argument('--mermaid-source', action='store_true',
                    help='kèm nguồn mermaid trong macro Expand dưới ảnh')
    args = ap.parse_args()

    out_dir = os.path.abspath(args.out)
    img_dir = os.path.join(out_dir, 'images')
    os.makedirs(img_dir, exist_ok=True)

    manifest = []
    for path in args.files:
        slug = os.path.splitext(os.path.basename(path))[0]
        with open(path, encoding='utf-8') as fh:
            src = fh.read()

        conv = Converter(slug, img_dir, args.mermaid_format, args.mermaid_source)
        body = conv.convert(src)

        head = ''
        if args.toc:
            head = ('<ac:structured-macro ac:name="toc" ac:schema-version="1">'
                    '<ac:parameter ac:name="maxLevel">3</ac:parameter>'
                    '<ac:parameter ac:name="minLevel">2</ac:parameter>'
                    '<ac:parameter ac:name="outline">true</ac:parameter>'
                    '<ac:parameter ac:name="style">none</ac:parameter>'
                    '</ac:structured-macro>\n')

        dest = os.path.join(out_dir, slug + '.storage.html')
        with open(dest, 'w', encoding='utf-8') as fh:
            fh.write(head + body + '\n')

        # ghi nguồn mermaid ra .mmd để render riêng
        for fname, source in conv.diagrams:
            mmd = os.path.join(img_dir, os.path.splitext(fname)[0] + '.mmd')
            with open(mmd, 'w', encoding='utf-8') as fh:
                fh.write(source + '\n')

        manifest.append((slug, dest, [f for f, _ in conv.diagrams]))
        print('%-28s -> %-38s %2d sơ đồ  %6.1f KB'
              % (os.path.basename(path), os.path.basename(dest),
                 len(conv.diagrams), os.path.getsize(dest) / 1024))

    with open(os.path.join(out_dir, 'MANIFEST.txt'), 'w', encoding='utf-8') as fh:
        for slug, dest, imgs in manifest:
            fh.write('%s\n  file: %s\n  attachments: %s\n\n'
                     % (slug, os.path.basename(dest),
                        ', '.join(imgs) if imgs else '(không có)'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
