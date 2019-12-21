#!/bin/bash

# Train the Tarteel dataset on DeepSpeech.
# Expects you have the following:
#   1. Train/Dev/Test CSV splits
#   2. An alphabet.txt file
#   3. A binary language model
#   4. A compiled language model trie

check_file(){
  if [[ -f $1 ]]; then
    echo "Found $1"
  fi
}

check_files(){
  for var in "$@"
  do
    check_file "$var"
  done
}

check_pyenv(){
  INVENV=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')
  if [[ INVENV -eq 0 ]]; then
    echo "Not in a virtual environment. Make sure you activate a virtual environment."
    exit 0
  fi
}

TARTEEL_DEEPSPEECH_DATA_DIR="data/tarteel"
TRAIN_CSV_FILE="$TARTEEL_DEEPSPEECH_DATA_DIR/train.csv"
DEV_CSV_FILE="$TARTEEL_DEEPSPEECH_DATA_DIR/dev.csv"
TEST_CSV_FILE="$TARTEEL_DEEPSPEECH_DATA_DIR/test.csv"

EXPORT_DIR="$TARTEEL_DEEPSPEECH_DATA_DIR/results/model_export/"
CHECKPOINT_DIR="$TARTEEL_DEEPSPEECH_DATA_DIR/results/checkout/"
LOG_DIR="$TARTEEL_DEEPSPEECH_DATA_DIR/results/logs/"
SUMMARY_DIR="$TARTEEL_DEEPSPEECH_DATA_DIR/results/summary/"

ALPHABET_PATH="$TARTEEL_DEEPSPEECH_DATA_DIR/alphabet.txt"
LM_BINARY_PATH="$TARTEEL_DEEPSPEECH_DATA_DIR/lm.binary"
LM_TRIE_PATH="$TARTEEL_DEEPSPEECH_DATA_DIR/quran.trie"

check_pyenv
check_files ALPHABET_PATH LM_BINARY_PATH LM_TRIE_PATH TRAIN_CSV_FILE DEV_CSV_FILE TEST_CSV_FILE
echo "Export DIR: $EXPORT_DIR"
echo "Checkpoint DIR: $CHECKPOINT_DIR"

python3 -u DeepSpeech.py \
  --log_dir "$LOG_DIR" \
  --summary_dir "$SUMMARY_DIR" \
  --alphabet_config_path "$ALPHABET_PATH" \
  --checkpoint_dir "$CHECKPOINT_DIR" \
  --train_files "$TRAIN_CSV_FILE" \
  --dev_files "$DEV_CSV_FILE" \
  --test_files "$TEST_CSV_FILE" \
  --export_dir "$EXPORT_DIR" \
  --lm_binary_path "$LM_BINARY_PATH" \
  --lm_trie_path "$LM_TRIE_PATH" \
  --lm_alpha 1.5 \
  --dropout_rate 0.30 \
  --train_batch_size 1 \
  --dev_batch_size 1 \
  --test_batch_size 1 \
  --n_hidden 2048 \
  --epochs 35 \
  --early_stop true \
  --es_steps 6 \
  --es_mean_th 0.1 \
  --es_std_th 0.1 \
  --learning_rate 0.00095 \
  "$@"
