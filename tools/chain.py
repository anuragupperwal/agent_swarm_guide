"""chain.py <guide dir>: verify the prev/next pager chain, header metadata and reading times."""
import os, re, sys

g = sys.argv[1]
idx = open(os.path.join(g, "index.html"), encoding="utf-8").read()
chs = sorted(f for f in os.listdir(os.path.join(g, "chapters")) if f.endswith(".html"))
order = ["index.html"] + ["chapters/" + c for c in chs] + ["glossary.html"]
problems = []
for i, page in enumerate(order[1:], start=1):
    src = open(os.path.join(g, page), encoding="utf-8").read()
    base = os.path.dirname(page)
    pager = re.search(r'<nav class="pager".*?</nav>', src, re.S)
    if not pager:
        problems.append(f"{page}: no pager"); continue
    links = dict(re.findall(r'<a class="(prev|next)" href="([^"]+)"', pager.group(0)))
    want_prev = os.path.relpath(order[i - 1], base or ".")
    want_next = os.path.relpath(order[i + 1] if i + 1 < len(order) else "index.html", base or ".")
    if links.get("prev") != want_prev:
        problems.append(f"{page}: prev is {links.get('prev')}, expected {want_prev}")
    if links.get("next") != want_next:
        problems.append(f"{page}: next is {links.get('next')}, expected {want_next}")
    if page.startswith("chapters/"):
        num = os.path.basename(page)[:2]
        dc = re.search(r'id="done-toggle" data-chapter="(\d\d)"', src)
        if not dc or dc.group(1) != num:
            problems.append(f"{page}: done toggle data-chapter is {dc.group(1) if dc else None}")
        t = re.search(r'<li><b>(\d+) min</b>', src)
        words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<svg.*?</svg>", " ", src, flags=re.S)).split())
        row = re.search(r'href="%s".*?</a>' % re.escape(page), idx, re.S)
        home_t = re.search(r'(\d+) min', row.group(0)) if row else None
        print(f"{num}: {words:5d} words · page says {t.group(1) if t else '-':>4} min · home says {home_t.group(1) if home_t else '-':>4} min")
print("\n".join(problems) or "pager chain and done toggles: OK")
