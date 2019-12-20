import os
from os import path
from typing import Union

from util import file_handler
from util.logging import print_warn

QURAN_FILE = path.join(path.dirname(os.getcwd()), 'data/quran.json')
MAX_SURAH_NUMBER = 114
MIN_SURAH_NUMBER = 1


class Quran:

    def __init__(self, quran_file: str = QURAN_FILE):
        self._quran_json = file_handler.open_json(quran_file)

    def get_quran(self):
        return self._quran_json

    def surah(self, surah_number: int) -> Union[dict, None]:
        if (surah_number > MAX_SURAH_NUMBER) or (surah_number < MIN_SURAH_NUMBER):
            print_warn('Surah number out of bounds')
            return None
        try:
            surah = self._quran_json[str(surah_number)]
            return surah
        except KeyError:
            print_warn('Surah number not found')
            return None

    def ayah(self, surah_number: int, ayah_number: int) -> Union[dict, None]:
        try:
            ayah = self.surah(surah_number)[str(ayah_number)]
            return ayah
        except KeyError:
            print_warn('Ayah not found')
            return None

    def get_ayah_text(self,
                      surah_number: int,
                      ayah_number: int,
                      uthmani: bool = False) -> Union[str, None]:
        result = self.ayah(surah_number, ayah_number)
        if result:
            if uthmani:
                return result.get('displayText')
            else:
                return result.get('text')
        else:
            return result

