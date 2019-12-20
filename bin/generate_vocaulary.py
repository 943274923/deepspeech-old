import os
from os import path

from ..util import quran

alphabet_path = path.join(path.dirname(os.getcwd()), 'data/tarteel/vocabulary.txt')


def main():
    q = quran.Quran()
    with open(alphabet_path, 'w') as file:
        for surah_number in range(1, quran.MAX_SURAH_NUMBER+1):
            ayahs = q.surah(surah_number)
            for ayah_number in ayahs:
                text = q.get_ayah_text(surah_number, ayah_number)
                file.write("%s\n" % text)


if __name__ == '__main__':
    main()
