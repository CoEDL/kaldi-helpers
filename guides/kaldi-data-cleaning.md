# Cleaning data for Kaldi

ASR systems train on existing transcribed material, building a model using the speech data, which can then be applied to untranscribed speech. The system learns using a lexicon, which our script will generate. However, we need to seed the lexicon with a phone set that contains representations for all the speech signals in our data.

The more pre-transcribed speech data you have to train with, the better your results will be. These systems typically train on hundreds of hours of pre-transcribed data, so let's see how well we go with what we have. 

It is important to recognise that the type of speech that the system trains with will determine the type of speech that the trained model can be applied to, for example if you train a system with speech of a single person counting numbers, that model will be great at automatically transcribing more speech of that person counting, but wouldn't be practical for transcribing a different person storytelling.

## Preparing your existing transcriptions

Choose a set of data from your corpus. Look for already-transcribed content from a single or multiple speakers, prefereably with more than an hour of transcription. Select data that is of a common recording activity, e.g. short sentences, or stories. The scripts we are using are written to work with ELAN files. Clean your transcriptions by looking through them and checking the following, note that it can be worth duplicating your existing transcription tiers to prepare clean transcription data for the system and not lose your existing inline conventions etc...

- Reduce inconsistencies or typos in transcriptions.

- Standardise variation in spelling.

- Replace non-lexical number forms, sho
- rthand forms, abbreviations with full lexical forms. For example, replace numbers '9' with 'nine'.

- Code-switching in a single tier will confuse the system. Best to have separate tiers for each language, and train the system on just one of the languages.

- Out-of-vocabulary words (words that are in the corpus but not in the lexicon) will reduce the accuracy. Ensure that everything in the speech signal is transcribed.

- Remove inline conventions such as speaker or language codes.


## Cleaning audio 

As well as cleaning the transcription, ensure the audio is in a standard format. The scripts anticipate 41.KHz 16bit mono audio. If needed, you can convert audio to this format using [Switch](http://www.nch.com.au/switch/index.html) (OSX) or [Audacity](http://www.audacityteam.org/) 


## Pronunciation mapping

A pronunciation dictionary mapping the orthography to phones will be used to build the training lexicon. See below for an example. Note that the sound symbol isn't an IPA symbol, it is just a character that can be used internally to uniquely identify that speech signal. Begin by listing your orthography's graphemes and digraphs. Then write a corresponding symbol for each, using only hyphen plus lowercase and capital a-z. Ensure that the symbols are unique within the list.

```
# Initial mapping of consonant graphemes and digraphs
c c
h h
kw k_w
k k
b m_b
d n_d
nz n_dz
z ts
th D
t t
s s
ŋ N
y j
w w

# Vowels
i i
ü y
u u
e e 
o o
```

You should now have a collection of cleaned transcriptions, audio in the right format, and a mapping file of the letters to the sounds for the language.
