# Tarteel DeepSpeech

Tarteel's fork of DeepSpeech with scripts and utilities to use the Tarteel dataset.

## Setup

### Regular setup

Create a virtual environment.
We use one named `ds-env`.

```bash
workon ds-env
pip3 install tensorflow-gpu==1.14.0
pip3 install -r requirements.txt
pip3 install $(python3 util/taskcluster.py --decoder)
./DeepSpeech.py --helpfull
```

### Building from source

If you have a GPU, make sure to say yes to Cuda in the Tensorflow config step.
The table of compute capabilities can be found [here](https://developer.nvidia.com/cuda-gpus#compute).

```bash
# Use a venv and a workspace
workon ds-env
mkdir ds_ws && cd ds_ws
# Setup bazel
git clone https://github.com/bazelbuild/bazelisk.git
ln -s /usr/local/bin/bazel ~/ds_ws/bazelisk/bazelisk.py
export USE_BAZEL_VERSION=0.24.1
cd ..
# Get DS and TF
git clone https://github.com/mozilla/DeepSpeech/
git clone https://github.com/mozilla/tensorflow
cd tensorflow && git checkout r1.14
# Use defaults, yes to Cuda
./configure
# Assuming you cloned everything in the same directory
ln -s ../DeepSpeech/native_client ./
bazel build --workspace_status_command="bash native_client/bazel_workspace_status_cmd.sh" \
            --config=monolithic --config=cuda -c opt --copt=-O3 --copt="-D_GLIBCXX_USE_CXX11_ABI=0" \
            --copt=-fvisibility=hidden //native_client:libdeepspeech.so //native_client:generate_trie
cd ~/ds_ws/DeepSpeech/native_client
export TFDIR=~/ds_ws/tensorflow
make deepspeech
PREFIX=/usr/local sudo make install
```

### Preparing language model

To generate language models, use [`KenLM`]

```bash
# Ubuntu
sudo apt-get install build-essential libboost-all-dev cmake zlib1g-dev libbz2-dev liblzma-dev 
# Mac OS
brew install cmake boost zlib

wget -O - https://kheafield.com/code/kenlm.tar.gz |tar xz
mkdir kenlm/build && cd kenlm/build
cmake ..
make -j 4
# Optionally, add bin to path
export PATH=$PATH:$HOME/kenlm/build/bin
```

Create the alphabet and vocabulary

```bash
python bin/generate_alphabet.py
python bin/generate_vocabulary.py
```

Create the `arpa` file for the binary build

```bash
lmplz --text data/tarteel/vocabulary.txt --arpa  data/tarteel/words.arpa --o 4
build_binary trie -q 16 -b 7 data/tarteel/words.arpa data/tarteel/lm.binary
# Assuming you compiled DeepSpeech
<path-to-deepspeech>/native_client/generate_trie data/tarteel/alphabet.txt \
                                                 data/tarteel/lm.binary \
                                                 data/tarteel/vocabulary.txt quran.trie
```

## Usage

* [`generate_alphabet.py`] Creates the `alphabet.txt` file used for the language model.
* [`generate_vocabulary`] Creates the `vocabulary.txt` file used for the language model.
* [`train_deepspeech.sh`] Starts training DeepSpeech.
Directories in the script need to be configured.

[`generate_alphabet`]: bin/generate_alphabet.py
[`generate_vocabulary]: bin/generate_vocaulary.py
[`train_deepspeech.sh`]: bin/train_deepspeech.sh
[`KenLM`]: https://kheafield.com/code/kenlm/
