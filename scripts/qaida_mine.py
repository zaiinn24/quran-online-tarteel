"""Find practice words and phrases in the Quran (King Fahd Uthmani text, normalised by quran_text.fix) for the Qaida.
Every word returned is copied exactly from the Quran, with its surah:ayah reference."""
import json, os, re, collections
from quran_text import fix

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = json.load(open(os.path.join(ROOT, "data", "quran-uthmani.json")))

F, K, D = "َ", "ِ", "ُ"
FT, KT, DT = "ً", "ٍ", "ٌ"
OFT, ODT, OKT = "ࣰ", "ࣱ", "ࣲ"
SUK, SHAD, MADD, KZ = "ۡ", "ّ", "ٓ", "ٰ"
SHORT = {F, K, D}
TAN = {FT, KT, DT, OFT, ODT, OKT}
STOP = "ۖۗۘۙۚۛۜ۞۩"
LET = set("بتثجحخدذرزسشصضطظعغفقكلمنهويءأإؤئة") | {"ا"}

WORDS = collections.Counter()
REF = {}
PAIRS = []      # (w1, w2, surah, ayah)
for s in Q:
    for v in s["verses"]:
        ws = [w for w in fix(v["text"]).split(" ") if w and w not in STOP]
        clean = [w.strip(STOP) for w in ws]
        for w in clean:
            WORDS[w] += 1
            REF.setdefault(w, (s["id"], v["id"]))
        for a, b in zip(clean, clean[1:]):
            PAIRS.append((a, b, s["id"], v["id"]))


def units(w):
    u = []
    for c in w:
        if c in LET or c in "ٱآى":
            u.append([c, ""])
        elif u:
            u[-1][1] += c
        else:
            return None
    return u


def pick(pred, n, minlen=2, maxlen=5, exclude=()):
    out = []
    for w, _ in WORDS.most_common():
        u = units(w)
        if not u or not (minlen <= len(u) <= maxlen) or w in exclude:
            continue
        if any(c in "ٱآى" for c, _ in u):
            continue
        if pred(u):
            out.append(w)
            if len(out) >= n:
                break
    return out


def simple(m):
    return m in SHORT


# --- lesson filters ---
harakat = lambda n: pick(lambda u: all(simple(m) for c, m in u) and u[-1][0] != "ة", n, 3, 4)


def tanween(n):
    def ok(u):
        body, last = u[:-1], u[-1]
        if last[0] == "ا" and not last[1]:   # fathatan + alif
            body, last = u[:-2], u[-2]
        return len(body) >= 1 and all(simple(m) for c, m in body) and len(last[1]) == 1 and last[1] in TAN
    return pick(ok, n, 2, 5)


def _madd_ok(u, need_madd=True):
    has = False
    i = 0
    while i < len(u):
        c, m = u[i]
        if not m:
            prev = u[i - 1][1] if i else ""
            if (c == "ا" and prev == F) or (c == "و" and prev == D) or (c == "ي" and prev == K):
                has = True
                i += 1
                continue
            return False
        if not (simple(m) or (m in TAN and i == len(u) - 1)):
            return False
        i += 1
    return has or not need_madd


madd = lambda n: pick(lambda u: _madd_ok(u), n, 3, 5)
khari = lambda n: pick(lambda u: any(KZ in m for c, m in u) and all(m in SHORT or m == F + KZ or m == KZ or (m in TAN) or (m == "" and c in "اوي") for c, m in u), n, 2, 5)


def leen(n):
    def ok(u):
        has = False
        for i, (c, m) in enumerate(u):
            if c in "وي" and m == SUK and i and u[i - 1][1] == F:
                has = True
            elif not (simple(m) or (m in TAN and i == len(u) - 1)):
                return False
        return has
    return pick(ok, n, 2, 5)


def sukoon(n):
    def ok(u):
        has = False
        for i, (c, m) in enumerate(u):
            if m == SUK and i > 0 and c not in "وي":
                has = True
            elif not (simple(m) or (m in TAN and i == len(u) - 1)):
                return False
        return has and u[0][1] != SUK
    return pick(ok, n, 2, 5)


def shadda(n, two=False):
    def ok(u):
        k = 0
        for i, (c, m) in enumerate(u):
            if SHAD in m:
                rest = m.replace(SHAD, "")
                if rest not in SHORT and rest not in TAN:
                    return False
                k += 1
            elif not (simple(m) or m == SUK or (m in TAN and i == len(u) - 1) or (m == "" and c in "اوي" and i and u[i - 1][1][-1:] in (F, D, K))):
                return False
        return k >= (2 if two else 1) and SHAD not in u[0][1]
    return pick(ok, n, 2, 6)


def madd_sign(n):
    return pick(lambda u: any(MADD in m for c, m in u) and any(c in "ءأإؤئ" for c, m in u), n, 3, 6)


def qalqala(n):
    return pick(lambda u: any(c in "قطبجد" and m == SUK for c, m in u) and all(simple(m) or m == SUK or (m in TAN) or m == "" for c, m in u), n, 2, 5)


def ghunna(n):
    return pick(lambda u: any(c in "نم" and SHAD in m for c, m in u), n, 2, 5)


def silent(n):
    return pick(lambda u: any("۟" in m for c, m in u), n, 3, 7)


# --- phrase rules (two words) ---
IZHAR, IDGHAM, IQLAB = set("ءهعحغخأإ"), set("يرملون"), set("ب")


def ends_noon_or_tanween(w):
    u = units(w)
    if not u:
        return None
    c, m = u[-1]
    if c == "ا" and not m and len(u) > 1:
        c, m = u[-2]
    if any(t in m for t in TAN):
        return "tanween"
    if c == "ن" and (m in ("", SUK, "ۢ")):
        return "noon"
    return None


def noon_rules(per=6):
    out = {"izhar": [], "idgham": [], "iqlab": [], "ikhfa": []}
    seen = set()
    for a, b, s, v in PAIRS:
        kind = ends_noon_or_tanween(a)
        if not kind or b.startswith("ٱ") or len(a) > 9 or len(b) > 9:
            continue
        f = b[0]
        rule = "izhar" if f in IZHAR else "idgham" if f in IDGHAM else "iqlab" if f in IQLAB else "ikhfa"
        key = (rule, f, kind) if rule in ("izhar", "idgham", "ikhfa") else (rule, a, b)
        if key in seen or len(out[rule]) >= per:
            continue
        seen.add(key)
        out[rule].append((a, b, s, v, kind))
    return out


def meem_rules(per=4):
    out = {"ikhfa": [], "idgham": [], "izhar": []}
    seen = set()
    for a, b, s, v in PAIRS:
        u = units(a)
        if not u or u[-1][0] != "م" or u[-1][1] not in ("", SUK) or b.startswith("ٱ") or len(a) > 8 or len(b) > 8:
            continue
        f = b[0]
        rule = "ikhfa" if f == "ب" else "idgham" if f == "م" else "izhar"
        if rule == "izhar" and f in "ءأإ":
            pass
        key = (rule, f) if rule == "izhar" else (rule, a, b)
        if key in seen or len(out[rule]) >= per:
            continue
        seen.add(key)
        out[rule].append((a, b, s, v))
    return out


def allah(per=4):
    out = {"heavy": [], "light": []}
    for a, b, s, v in PAIRS:
        if re.sub("[\u064b-\u065f\u0670\u06d6-\u06ed\u08f0-\u08f2]", "", b) != "ٱلله":
            continue
        u = units(a)
        if not u or len(a) > 8:
            continue
        m = u[-1][1]
        if u[-1][0] == "ا" and not m and len(u) > 1:
            m = u[-2][1]
        kind = "light" if m.endswith(K) else ("heavy" if m.endswith(F) or m.endswith(D) else None)
        if kind and len(out[kind]) < per and (a, b) not in [(x[0], x[1]) for x in out[kind]]:
            out[kind].append((a, b, s, v))
    return out


def ra(n):
    heavy = pick(lambda u: any(c == "ر" and m in (F, D) for c, m in u) and all(simple(m) or m == "" for c, m in u), n, 3, 4)
    light = pick(lambda u: any(c == "ر" and m == K for c, m in u) and all(simple(m) or m == "" for c, m in u), n, 3, 4)
    return heavy, light


def waqf_examples():
    out = {}
    for s in Q:
        for v in s["verses"]:
            t = fix(v["text"])
            for sign in "ۘۙۚۖۗۛ":
                if sign in t and sign not in out:
                    ws = t.split(" ")
                    i = next(k for k, w in enumerate(ws) if sign in w)
                    out[sign] = (" ".join(ws[max(0, i - 2):i + 3]), s["id"], v["id"])
    return out


def wasl(n):
    out = []
    seen = set()
    for a, b, s, v in PAIRS:
        if b.startswith("ٱل") and len(a) <= 6 and len(b) <= 9 and b not in seen and a.endswith((F, D, K)):
            seen.add(b)
            out.append((a, b, s, v))
            if len(out) >= n:
                break
    return out


if __name__ == "__main__":
    print("harakat", harakat(30))
    print("tanween", tanween(24))
    print("madd", madd(30))
    print("khari", khari(12))
    print("leen", leen(12))
    print("sukoon", sukoon(30))
    print("shadda", shadda(24))
    print("shadda2", shadda(12, True))
    print("madd_sign", madd_sign(12))
    print("qalqala", qalqala(12))
    print("ghunna", ghunna(12))
    print("silent", silent(8))
    for k, v in noon_rules().items():
        print("noon", k, [(a + " " + b) for a, b, *_ in v])
    for k, v in meem_rules().items():
        print("meem", k, [(a + " " + b) for a, b, *_ in v])
    for k, v in allah().items():
        print("allah", k, [(a + " " + b) for a, b, *_ in v])
    print("ra", ra(8))
    print("waqf", waqf_examples())
    print("wasl", wasl(8))
