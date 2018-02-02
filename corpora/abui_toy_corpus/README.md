# Abui 'Toy' Corpus

The Abui toy corpus gives an example of the simplest configuration to run the default build routine using the kaldi-helpers toolkit.

## Contents

### `config`

The `config` folder contains three required files:

- `letter_to_sound.txt`: a pronunciation dictionary for mapping the orthography to phones
- `silence_phones.txt`: phones that indicate silences in all texts
- `optional_silence.txt`: as above, but ones not necessarily present in all texts

### `data`

The corpus consists of 5 pairs of .wav and .eaf files (`1_1_1.wav`, ..., `1_1_5.eaf`) in the `data` directory. In each .eaf file, there is a single tier with Abui text, as show below for `1_1_1.eaf`:

![](../../screenshots/abui-toy-corpus-eaf.png)

### `output`

An empty folder to which the kaldi-helper scripts will write their output.

## Usage

The easiest way to use kaldi-helpers is through the Docker image (see `/guides/kaldi-docker-setup`). With Docker set up and running, and the `coedl/kaldi-helpers` image on your computer, you can prepare the abui-toy-corpus data for use with Kaldi in the following way:

```bash
# Change ~/git-repos/coedl/kaldi-helpers/corpora/abui_toy_corpus/
# to the appropriate path for your computer

docker run --rm \
           -v ~/git-repos/coedl/kaldi-helpers/corpora/abui_toy_corpus/:/kaldi-helpers/input \
           coedl/kaldi-helpers:0.1 \
           task _run-elan-default
```

***Notes.***

- The `-v` option in the `docker run` command indicates the local folder `~/git-repos/coedl/kaldi-helpers/corpora/abui_toy_corpus` to be mounted into the container. **Adjust this path accordingly**. The rest of the string `:/kaldi-helpers/input` indicates the mount path *inside* the Docker container. **Do not change this path**. Thus your `-v` option should look like `C:\your\corpus\path:/kaldi-helpers/input` or `/Users/you/corpus/data/:/kaldi-helpers/input`
- It his highly recommended that you use a specific version of the `coedl/kaldi-helpers` Docker image for reproducibility purposes, e.g. `coedl/kaldi-helpers:0.1`.