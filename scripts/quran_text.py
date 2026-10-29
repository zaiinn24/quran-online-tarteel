"""The quran-json Uthmani text uses the KFGQPC font encoding. Map those code points to standard Unicode so that
standard Arabic fonts (Amiri) draw the right marks:
  U+0657 -> U+08F0 open fathatan, U+065E -> U+08F1 open dammatan, U+0656 -> U+08F2 open kasratan,
  U+0652 -> U+06DF small high rounded zero (letter written but not read, e.g. ءَامَنُوا۟)."""
_MAP = str.maketrans({"ٗ": "ࣰ", "ٞ": "ࣱ", "ٖ": "ࣲ", "ْ": "۟"})


def fix(text):
    return text.translate(_MAP)
