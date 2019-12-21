"""
Format audio files into CSV used by DeepSpeech.

DeepSpeech format is:

| wav_filename | wav_filesize     | transcript |
| ------------ | ---------------- | ---------- |
| ...          | ...              | ...        |

TODO(piraka9011)
- Use cache
- Use Python's logger
"""

import argparse
import os
from pathlib import Path
import re

import sox
from tqdm import tqdm
from typing import List, Set, Tuple, Union

from util import audio
from util import file_helper
from util import quran
from util import unicode_helper

DEEPSPEECH_FILENAME_HEADER = 'wav_filename'
DEEPSPEECH_FILESIZE_HEADER = 'wav_filesize'
DEEPSPEECH_TRANSCRIPT_HEADER = 'transcript'
DEEPSPEECH_CSV_HEADERS = [DEEPSPEECH_FILENAME_HEADER, DEEPSPEECH_FILESIZE_HEADER, DEEPSPEECH_TRANSCRIPT_HEADER]
DEEPSPEECH_ALPHABET_FILENAME = 'alphabet.txt'
DEEPSPEECH_CSV_FILENAME = 'tarteel_deepspeech_full.csv'
DEFAULT_CACHE_DIR = '/tmp'

parser = argparse.ArgumentParser(description='Prepare a CSV file for Deepspeech')
parser.add_argument(
    '-i', '--audio-directory', type=str, required=True,
    help='Path to directory with audio files .'
)
parser.add_argument(
    '-o', '--output-directory', type=str,
    help='Output directory for CSV and alphabet.txt.'
)
parser.add_argument(
    '--convert-audio', action='store_true',
    help='Run audio conversion for each file.'
)
args = parser.parse_args()
quran_helper = quran.Quran()


def check_args():
    audio_directory = Path(args.audio_directory)
    output_directory = Path(args.output_directory)
    if not audio_directory.is_dir():
        raise ValueError("Audio directory is not a valid directory.")
    if not output_directory.is_dir():
        raise ValueError("Output directory is not a valid directory.")
    print("Parameters:\nAudio Directory: {}\nOutput Directory: {}\n"
          "Convert Audio: {}".format(
        args.audio_directory, args.output_directory, args.convert_audio))


def get_surah_ayah_from_file(filename: str) -> Tuple[int, int]:
    split_filename = filename.split('_')
    surah_number = int(split_filename[0])
    ayah_number = int(split_filename[1])
    return surah_number, ayah_number


def normalize_arabic_text(text: str) -> str:
    text.strip()  # Remove trailing chars
    text = unicode_helper.space_out(text)  # Remove spaces and diacritics
    text = unicode_helper.normalize_arabic(text)
    return text


def create_csv_file(file_names: List) -> Tuple[List, Set]:
    csv_rows = [DEEPSPEECH_CSV_HEADERS]
    unique_alphabet = set()
    for wav_filename in tqdm(file_names):
        wav_filename = wav_filename.strip()  # Remove trailing characters
        file_path = Path(os.path.join(args.audio_directory, wav_filename))
        file_size = file_helper.get_file_size(file_path.as_posix())
        if not file_size:
            print('Could not get {} file size skipping...'.format(wav_filename))
            continue

        surah_number, ayah_number = get_surah_ayah_from_file(wav_filename)
        text = quran_helper.get_ayah_text(surah_number, ayah_number)
        text = normalize_arabic_text(text)  # Removes diacritics, spaces, etc.
        unique_alphabet = unique_alphabet | set(text)  # Collect set of unique characters
        try:
            if args.convert_audio:
                new_file_path = os.path.join(args.output_directory, 'recordings', wav_filename)
                audio.convert_audio(file_path.as_posix(), new_file_path, file_type='wav')
                file_path = Path(new_file_path)
            csv_row = [file_path.as_posix(), file_size, text]
            csv_rows.append(csv_row)
        except sox.core.SoxError as e:
            print("Caught Sox error, continuing...\n{}".format(e))


    csv_rows_cache = os.path.join(DEFAULT_CACHE_DIR, DEEPSPEECH_CSV_FILENAME + '.pkl')
    file_helper.dump_to_cache(csv_rows, csv_rows_cache)
    alphabet_cache = os.path.join(DEFAULT_CACHE_DIR, DEEPSPEECH_ALPHABET_FILENAME + '.pkl')
    file_helper.dump_to_cache(unique_alphabet, alphabet_cache)

    return csv_rows, unique_alphabet


def main():
    check_args()  # Throws if invalid args

    audio_directory = args.audio_directory
    file_names = file_helper.get_all_files_in_directory(audio_directory)
    csv_rows, unique_alphabet = create_csv_file(file_names)

    csv_file_path = os.path.join(args.output_directory, DEEPSPEECH_CSV_FILENAME)
    file_helper.write_csv(csv_file_path, csv_rows)
    alphabet_path = os.path.join(args.output_directory, DEEPSPEECH_ALPHABET_FILENAME)
    file_helper.write_to_text(alphabet_path, unique_alphabet)


if __name__ == '__main__':
    main()
