from pathlib import Path
import re
import string

ARABIC_DIACRITICS = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ   | # Tatwil/Kashida
                             ٓ    |
                             ۢ    |
                            ۦ     |
                            ۥ     |
                             ٔ    
                         """, re.VERBOSE)

ARABIC_PUNCTUATIONS = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''' + string.punctuation


def remove_diacritics(text: str) -> str:
    return re.sub(ARABIC_DIACRITICS, '', text)


def normalize_arabic(text: str) -> str:
    text = re.sub(" ٰ", " ا", text)
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text


def space_out(text: str) -> str:
    return re.sub("(.)", "\g<1> ", re.sub(" ", "_", re.sub(ARABIC_DIACRITICS, '', text)))


def remove_arabic_punctuation(text: str) -> str:
    translator = str.maketrans('', '', ARABIC_PUNCTUATIONS)
    return text.translate(translator)


def clean_url(url: str) -> Path:
    new_url = re.sub('(\?.*)', '', url)     # Remove the query params after
    link_re = re.compile('[^/]+(?=/$|$)')   # Remove the URL before
    new_url = link_re.search(new_url).group()
    return Path(new_url)

