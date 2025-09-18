import re


_ARABIC_TO_PERSIAN = str.maketrans({
    "ي": "ی",
    "ى": "ی",
    "ئ": "ی",
    "ك": "ک",
})


def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = text.strip()
    t = t.translate(_ARABIC_TO_PERSIAN)
    t = t.replace("\u200c", " ")  # half-space to space
    t = re.sub(r"\s+", " ", t)
    t = t.lower()
    # digits: Persian/Arabic to Latin
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    for i, d in enumerate(persian_digits):
        t = t.replace(d, str(i))
    for i, d in enumerate(arabic_digits):
        t = t.replace(d, str(i))
    return t


