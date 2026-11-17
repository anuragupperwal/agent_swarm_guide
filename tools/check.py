"""Static checks for the Loop to Swarm guide.

Usage: python3 -I check.py <guide_dir> [file ...]
Checks per HTML file: tag balance, duplicate ids, local links and #anchors,
url(#id) marker refs, classes not defined in assets/style.css, required
template parts.
"""
import os
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr"}
# SVG elements commonly self-closed; html.parser reports them via startendtag.
OPTIONAL_CLOSE = {"p", "li", "dt", "dd", "tr", "td", "th", "thead", "tbody", "option"}

REQUIRED = [
    ("topbar", r'class="topbar"'),
    ("theme toggle", r'id="theme-toggle"'),
    ("guide.js", r'assets/guide\.js'),
    ("style.css", r'assets/style\.css'),
    ("title", r"<title>[^<]+</title>"),
]
CHAPTER_REQUIRED = [
    ("ch-head", r'class="ch-head"'),
    ("where strip", r'class="where"'),
    ("predict box", r'box predict'),
    ("project box", r'box project'),
    ("quiz", r'class="quiz"'),
    ("sources", r'class="sources"'),
    ("recall card", r'recall-card'),
    ("done toggle", r'id="done-toggle"'),
    ("pager", r'class="pager"'),
    ("toc rail", r'data-toc'),
]


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.ids = {}
        self.classes = set()
        self.hrefs = []
        self.urlrefs = []
        self.figures = 0
        self.svgs = 0
        self.svg_no_label = 0
        self.in_svg = 0

    def _attrs(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids[d["id"]] = self.ids.get(d["id"], 0) + 1
        if "class" in d and d["class"]:
            for c in d["class"].split():
                self.classes.add(c)
        if tag == "a" and "href" in d:
            self.hrefs.append((d["href"], self.getpos()[0]))
        for k, v in d.items():
            if v and "url(#" in v:
                self.urlrefs += re.findall(r"url\(#([^)]+)\)", v)
            if k in ("href", "xlink:href") and v and v.startswith("#") and tag == "use":
                self.urlrefs.append(v[1:])
        if tag == "svg":
            self.svgs += 1
            if d.get("role") != "img" or not d.get("aria-label"):
                self.svg_no_label += 1
        if tag == "figure":
            self.figures += 1

    def handle_starttag(self, tag, attrs):
        self._attrs(tag, attrs)
        if tag in VOID:
            return
        self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        self._attrs(tag, attrs)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        # pop optional-close elements implicitly
        while self.stack and self.stack[-1][0] != tag and self.stack[-1][0] in OPTIONAL_CLOSE:
            self.stack.pop()
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        self.errors.append(f"line {self.getpos()[0]}: </{tag}> does not match open "
                           f"<{self.stack[-1][0] if self.stack else 'none'}> "
                           f"(opened line {self.stack[-1][1] if self.stack else '-'})")
        # try to recover: pop to matching tag if present
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def css_classes(css_path):
    css = open(css_path, encoding="utf-8").read()
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return set(re.findall(r"\.([A-Za-z_][\w-]*)", css))


def check(guide, path, defined):
    rel = os.path.relpath(path, guide)
    src = open(path, encoding="utf-8").read()
    p = Parser()
    p.feed(src)
    p.close()
    out = []
    out += p.errors[:15]
    leftovers = [t for t in p.stack if t[0] not in OPTIONAL_CLOSE | {"html", "body", "head"}]
    if leftovers:
        out.append("unclosed: " + ", ".join(f"<{t}> line {l}" for t, l in leftovers[:10]))
    dups = [i for i, n in p.ids.items() if n > 1]
    if dups:
        out.append("duplicate ids: " + ", ".join(dups[:20]))
    missing_refs = sorted(set(r for r in p.urlrefs if r not in p.ids))
    if missing_refs:
        out.append("url(#id) refs with no target: " + ", ".join(missing_refs))
    base = os.path.dirname(path)
    for href, line in p.hrefs:
        if re.match(r"^(https?:|mailto:|tel:)", href):
            out.append(f"line {line}: external link {href}")
            continue
        file_part, _, frag = href.partition("#")
        if file_part:
            target = os.path.normpath(os.path.join(base, file_part))
            if not os.path.exists(target):
                out.append(f"line {line}: missing file {href}")
                continue
            if frag:
                tsrc = open(target, encoding="utf-8").read()
                if not re.search(r'id="%s"' % re.escape(frag), tsrc):
                    out.append(f"line {line}: missing anchor {href}")
        elif frag and frag not in p.ids:
            out.append(f"line {line}: missing anchor #{frag}")
    undefined = sorted(c for c in p.classes if c not in defined)
    if undefined:
        out.append("classes not in style.css: " + ", ".join(undefined))
    req = REQUIRED + (CHAPTER_REQUIRED if "/chapters/" in path else [])
    for name, pat in req:
        if not re.search(pat, src):
            out.append(f"missing template part: {name}")
    if p.svg_no_label:
        out.append(f"{p.svg_no_label} svg(s) without role=img + aria-label")
    if re.search(r"\$\s?\d", src):
        out.append("possible price ($digit) found")
    words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<svg.*?</svg>", " ", src, flags=re.S)).split())
    summary = f"{rel}: {len(src)//1024} KB, ~{words} words, {p.figures} figures, {p.svgs} svgs"
    return summary, out


def main():
    guide = sys.argv[1]
    defined = css_classes(os.path.join(guide, "assets", "style.css"))
    files = sys.argv[2:]
    if not files:
        files = [os.path.join(guide, "index.html")]
        g = os.path.join(guide, "glossary.html")
        if os.path.exists(g):
            files.append(g)
        chd = os.path.join(guide, "chapters")
        files += sorted(os.path.join(chd, f) for f in os.listdir(chd) if f.endswith(".html"))
    bad = 0
    for f in files:
        summary, problems = check(guide, os.path.abspath(f), defined)
        print(summary)
        for pr in problems:
            print("   - " + pr)
        bad += bool(problems)
    print(f"\n{len(files)} files, {bad} with findings")


if __name__ == "__main__":
    main()
