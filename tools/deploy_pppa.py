"""Deploy dist/sg-data.js, dist/axes-bundle.json, dist/reference-strategies.json and the
schema files to pppa.lv and make the generator load them.

Runs with Windows python on Kojusalas (the docroot is on the Windows side):

    python tools\\deploy_pppa.py  [--repo <path to this repo>] [--docroot C:\\WebServers\\Home\\pppa\\www]

Idempotent. First run (s1450) also removes the embedded AX/C/T/W block from
sg-app.js and adds the <script> tag to both generator pages. Backups go to
C:\\WebServers\\_backups_offweb\\pppa\\<tag>\\ (never into the docroot).
"""
import argparse, os, re, shutil, sys, datetime

ap = argparse.ArgumentParser()
ap.add_argument("--repo", default=r"\\wsl.localhost\Ubuntu-24.04\home\rihards\AI-strategy-generator")
ap.add_argument("--docroot", default=r"C:\WebServers\Home\pppa\www")
ap.add_argument("--tag", default="s1450")
args = ap.parse_args()

ROOT, BAK = args.docroot, os.path.join(r"C:\WebServers\_backups_offweb\pppa", args.tag)
JS = os.path.join(ROOT, "assets", "js")
# s1455: one bilingual page; the old LV/EN pages 301 to it
PAGES = [os.path.join(ROOT, "ai-strategy-generator.html")]


def read(p):
    b = open(p, "rb").read()
    return b[3:].decode("utf-8") if b.startswith(b"\xef\xbb\xbf") else b.decode("utf-8")


def write(p, s):
    rel = os.path.relpath(p, ROOT)
    dst = os.path.join(BAK, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy2(p, dst)
    open(p, "wb").write(s.encode("utf-8"))
    print("updated", rel)


# 1) sg-data.js from the repo's dist/
src = os.path.join(args.repo, "dist", "sg-data.js")
dst = os.path.join(JS, "sg-data.js")
new = read(src)
if not os.path.exists(dst) or read(dst) != new:
    if os.path.exists(dst):
        write(dst, new)
    else:
        open(dst, "wb").write(new.encode("utf-8"))
        print("installed assets/js/sg-data.js")
else:
    print("sg-data.js unchanged")

# 1b) axes bundle + reference + schema (read by api/strategija.php and served for reference)
for src_rel, dst_rel in (("dist/axes-bundle.json", "assets/data/axes-bundle.json"),
                         ("dist/reference-strategies.json", "assets/data/reference-strategies.json"),
                         ("schema/ai-strategy.xsd", "assets/schema/ai-strategy.xsd"),
                         ("schema/ai-strategy.schema.json", "assets/schema/ai-strategy.schema.json")):
    sp, dp = os.path.join(args.repo, *src_rel.split("/")), os.path.join(ROOT, *dst_rel.split("/"))
    content = read(sp)
    if not os.path.exists(dp) or read(dp) != content:
        os.makedirs(os.path.dirname(dp), exist_ok=True)
        if os.path.exists(dp): write(dp, content)
        else: open(dp, "wb").write(content.encode("utf-8")); print("installed", dst_rel)
    else:
        print(dst_rel, "unchanged")

# 2) strip the embedded data block from sg-app.js (first run only)
app = os.path.join(JS, "sg-app.js")
s = read(app)
m1 = re.search(r"^const AX=\[", s, re.M)
m2 = re.search(r'^let L="lv"', s, re.M)
if m1 and m2 and m1.start() < m2.start():
    # keep the AXES comment header that precedes `const AX=`
    head = s[:m1.start()]
    note = ('/* AX, C, T, W are declared in sg-data.js, generated from data/*.yaml in\n'
            '   https://github.com/rg4444/AI-strategy-generator — edit the YAML, not this file. */\n')
    s2 = head + note + s[m2.start():]
    for name in ("AX", "C", "T", "W"):
        assert not re.search(rf"^const {name}=", s2, re.M), name
    write(app, s2)
    print(f"sg-app.js: removed {s.count(chr(10)) - s2.count(chr(10))} lines of embedded data")
elif m1:
    sys.exit("sg-app.js: unexpected layout (const AX found but no `let L=` after it)")
else:
    print("sg-app.js already split")

# 3) pages: load sg-data.js before sg-app.js; fix the axis count in copy
REPL = [
    ('<script src="/assets/js/sg-app.js"></script>',
     '<script src="/assets/js/sg-data.js"></script>\n<script src="/assets/js/sg-app.js"></script>'),
    ("pēc 17 lēmumu asīm", "pēc 20 lēmumu asīm"),
    ("septiņpadsmit lēmumu asis", "divdesmit lēmumu asis"),
    ("across 17 decision axes", "across 20 decision axes"),
    ("seventeen decision axes", "twenty decision axes"),
]
for p in PAGES:
    s = read(p)
    s2 = s
    if "sg-data.js" not in s2:
        s2 = s2.replace(*REPL[0])
    for a, b in REPL[1:]:
        s2 = s2.replace(a, b)
    if s2 != s:
        assert s2.count("sg-data.js") == 1 and s2.index("sg-data.js") < s2.index("sg-app.js")
        write(p, s2)
    else:
        print("unchanged", os.path.relpath(p, ROOT))
print("done")
