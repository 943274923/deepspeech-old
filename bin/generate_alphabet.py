import os
from os import path

from ..util import quran

alphabet_path = path.join(path.dirname(os.getcwd()), 'data/tarteel/alphabet.txt')


def main():
    q = quran.Quran()
    alphabet = set()
    for surah_number in range(1, quran.MAX_SURAH_NUMBER+1):
        ayahs = q.surah(surah_number)
        for ayah_number in ayahs:
            text = q.get_ayah_text(surah_number, ayah_number)
            alphabet = alphabet | set(text)

    with open(alphabet_path, 'w') as file:
        for letter in alphabet:
            file.write("%s\n" % letter)


if __name__ == '__main__':
    main()
