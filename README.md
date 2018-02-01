# CoEDL Kaldi pipeline

A set of scripts to use in preparing a corpus for speech-to-text processing with Kaldi.

Read about [setting up Docker](guides/kaldi-docker-setup.md) to run all this.

For more information about data requirements, see the [data guide](guides/2018-worskhop-preparation.md).

Read about the [tasks](guides/about-the-tasks.md) that can be run.


# Workflow

![Kaldi pipeline](https://g.gravizo.com/source/custom_mark?https%3A%2F%2Fraw.githubusercontent.com%2Fcoedl%2Fkaldi-helpers%2Fmaster%2FREADME.md)

 <details> 
  custom_mark
  digraph G {
    f1 [label="Format 1: Elan"]
    f2 [label="Format 2: Transcriber"]
    f3 [label="Format 3: Praat"]
    conversion [shape="box", label="Conversion", fontsize="20"]
    standard   [shape="box", label="Standard format. JSON file"]
    normalise  [shape="box", label="Normalisation", fontsize="20"]
    norm_model [label="Normalisation rules"]
    pronunciation [shape="box", label="Pronunication", fontsize="20"]
    pron_model [label="Pronunciation rules"]
    kaldi      [shape="box", label="Kaldi", fontsize="20"]
    \
    f1 -> conversion
    f2 -> conversion
    f3 -> conversion
    conversion -> standard
    standard -> normalise [label="TEXT", fontcolor="green"]
    standard -> kaldi [label="AUDIO", fontcolor ="green"]
    norm_model -> normalise
    normalise -> pronunciation
    pron_model -> pronunciation
    pronunciation -> kaldi
  ;})
  custom_mark
</details>