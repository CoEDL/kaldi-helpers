# Kaldi Pipeline tasks

The pipeline uses go-task to run Python scripts for data cleaning and preparation, and to organise the cleaned data into the folders that Kaldi expects.

The first task to run is to resample audio to 16 bit 44.1KkHz (which is what the Kaldi config is set to).

If the audio files contain English or other non-target language, there are two processes that can strip these out.

The `silence-audio` task will look through a directory (and subdirectories) for .eaf files. In each file, it will look for a tier with a particular name. For all annotations on that tier, it will process a matching-named audio file, silencing the sections in the audio signal that correspond to each annotation. This script does not segment or export files, it overwrites the source audio.

The `slice-eafs` task will slice up audio and eaf files in the corpus, outputting separate audio and text files according to annotations on a particular tier. It will only output segments where there are annotations (if an utterance in a speech signal is not annotated it will not export it). And it can skip annotations that have particular values, or that have ref annotations on another tier. This task is intended more for Persephone than Kaldi, though it will also output a json file of the annotation value, start time, end time, speaker id and media name, in the format that other Kaldi pipeline tasks expect. It does not clean the text or strip punctutation, just passes the annotation values through as is. 

The next group of tasks (`clean-output-folder`, `tmp-makedir`, `make-kaldi-subfolders`) prepare the data folders for Kaldi.

Then, the `elan-to-json` task looks through a corpus, getting all annotations for all tiers, and writing annotation value, start time, end time, speaker id and media name into a json file. Again, this script doesn't do any cleaning.

For cleaning text, the `clean-json` task will filter out English text, punctuation, digits, text that is marked with particular tags (however, it doesn't alter the audio signal for these deletions) and can strip out values from a list of special_cases. English text is detected using the nltk words corpus (exculding an utterance if > 10% English), and the langid Python language identification system.

Cleaned data is then prepared for Kaldi by the `generate-kaldi-files` task, which splits up the json into kaldi files, makes the lexicon.txt pronunciation dictionary, and non-silence phone files. The files generated from this task are: 

- segments
- text
- spk2gender
- wav.scp
- utt2spk
- corpus.txt
- lexicon.txt
- nonsilence_phones.txt

Next, Kaldi configs are generated with `generate-kaldi-configs`, and populated using vars from the task runner's Taskvars.yml file. These configs set the sample frequency, frame length, low and high freq cutoff, num_ceps, and decode beam values.

The final task, `_train-test-default`, runs Kaldi's run.sh script.


The helper tasks are grouped by driver tasks, so a user would typically just do:

- task _run-all-default
- task _build-default
- task _train-test-default




## A little bit more detail about each task

`resample-audio`
Resamples audio to 16 bit 44.1 kHz WAV


`silence-audio`
Read a folder of Elan files (defined by the corpus path variable in taskvars),
Look in each .eaf file for a tier named 'Silence'.
For each annotation, silence any audio files that match the eaf filename, by the annotation start and end times.


`split-eafs`
Read Elan files, slices matching WAVs by start and end times of annotations on a particular tier, outputting separate clips and text. Skips annotations with value '`PUB' on the main tier, or annotations that have a ref annotation on the 'Silence' tier. The tier names and $PUB values can be passed in as command args.


`clean-output-folder`
`tmp-makedir`
`make-kaldi-subfolders`
Sets up the folders that Kaldi requires, in the output directory
    kaldi/data/local/dict
    kaldi/data/test
    kaldi/data/train
    kaldi/conf
    kaldi/local


`elan-to-json`
Writes a JSON file (tmp/cleaned_filtered.json), containing all the text, annotation times and speaker info from the Elan files in input/data/


`json-to-kaldi`
Reads the cleaned_filtered.json file,
Writes the data as files for Kaldi into tmp/json_splitted/
    segments
    transcripts
    speakers
    recordings
    utt2spk
    corpus


`make-wordlist`
Outputs a wordlist from the cleaned_filtered.json file to stdout


`make-prn-dict`
The wordlist output is piped to this script,
which writes the pronunciation file at tmp/lexicon.txt


`make-nonsil-phones`
Gets the non-silence phones and saves as to tmp/nonsilence_phones.txt


`generate-kaldi-configs`
    Builds Kaldi config files path.sh, mfcc.conf, decode.config
    for things like the sample rate, script paths etc
    using the values set in Taskvars.yml


`copy-generated-files`
`copy-phones-configs`
`copy-helper-scripts`
Move files from tmp to their rightful places for Kaldi business


`gather-wavs`
`extract-wavs`
Collect the audio data from the input folder to the processing folders

