from argparse import ArgumentParser
import os
from typing import List, Tuple

from sklearn.model_selection import train_test_split

from util import file_helper

DEFAULT_RANDOM_SEED = 42
TRAIN_SPLIT_FRACTION = 0.6
TEST_SPLIT_FRACTION = 0.2
VALIDATION_SPLIT_FRACTION = 0.2

parser = ArgumentParser(description='CSV Data Train-Test-Validation Splitter')
parser.add_argument(
    '-i', '--input-file', type=str, required=True,
    help='Input to DeepSpeech CSV file'
)
parser.add_argument(
    '-o', '--output-dir', type=str, required=True,
    help='Directory to output split files'
)
parser.add_argument(
    '--train-fraction', type=float, default=TRAIN_SPLIT_FRACTION
)
parser.add_argument(
    '--test-fraction', type=float, default=TEST_SPLIT_FRACTION
)
parser.add_argument(
    '--validate-fraction', type=float, default=VALIDATION_SPLIT_FRACTION
)
parser.add_argument(
    '-s', '--seed', type=int, default=DEFAULT_RANDOM_SEED,
    help='Random seed for the split'
)
args = parser.parse_args()


def sum_is_one(*num_args: float):
    return sum(i for i in num_args) == 1.0


def create_train_test_validation_split(
        train_fraction: float,
        test_fraction: float,
        validate_fraction: float,
        data: List) -> Tuple[List, List, List]:
    if not sum_is_one(train_fraction, test_fraction, validate_fraction):
        raise ValueError("Split fractions do not sum to one!")

    # Splitting will be done in two steps, so identify the proper fractions for them.
    first_split_fraction = train_fraction + validate_fraction
    second_split_fraction = 1.0 - (validate_fraction / first_split_fraction)

    X_train_valid, X_test = train_test_split(
        data, train_size=first_split_fraction, random_state=args.seed, shuffle=True)
    X_train, X_valid = train_test_split(
        X_train_valid, train_size=second_split_fraction, random_state=args.seed, shuffle=True)

    return X_train, X_test, X_valid


def main():
    file_name_tuple = (
        os.path.join(args.output_dir, 'train.csv'),
        os.path.join(args.output_dir, 'dev.csv'),
        os.path.join(args.output_dir, 'test.csv'))
    all_csv_data = file_helper.open_csv(args.input_file)
    # Remove header, but store it for later
    header = all_csv_data[0]
    all_csv_data.pop(0)

    split_tuple = create_train_test_validation_split(
        args.train_fraction, args.test_fraction, args.validate_fraction, all_csv_data)

    for i, split in enumerate(split_tuple):
        split.insert(0, header)  # Put the header back
        file_helper.write_csv(file_name_tuple[i], split)
        print("Saved {}".format(file_name_tuple[i]))


if __name__ == '__main__':
    main()
