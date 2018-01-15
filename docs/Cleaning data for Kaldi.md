# Cleaning data for Kaldi

ASR systems will train on existing transcribed material, building a model using the speech data, which can then be applied to untranscribed speech. The system learns using a lexicon, which our script will generate. However, we need to seed the lexicon with a phone set that contains representations for all the speech signals in our data.

The more pre-transcribed speech data you have to train with, the better your results will be. These systems typically train on hundreds of hours of pre-transcribed data, so let's see how well we go with what we have. 

It is important to recognise that the type of speech that the system trains with will determine the type of speech that the trained model can be applied to, for example if you train a system with speech of a single person counting numbers, that model will be great at automatically trasncribing more speech of that person counting, but wouldn't be practical for transcribing a different person storytelling.

1) Preparing your existing transcriptions

Choose a set of data from your corpus. Look for similar content from a single or multiple speakers, prefereably with more than an hour of transcription. 

- Try to reduce inconsistencies or typos in transcriptions.

- Standardise variation in spelling.

- Replace non-lexical number forms, shorthand forms, abbreviations with full lexical forms. For example, replace numbers '9' with 'nine'.

- Code-switching in a single tier will confuse the system. Best to have separate tiers for each language, and train the system on just one language.

- Out-of-vocabulary words (words that are in the corpus but not in the lexicon) will reduce the accuracy. Ensure that everything in the speech signal is transcribed.

- Remove inline conventions such as speaker or language codes.

It can be worth duplicating your existing transcription tiers to prepare clean transcription data for the system and not lose your existing inline conventions etc.


2) As well as cleaning the transcription, ensure the audio is in a standard format - 41.KHz 16bit mono.

3) A pronunciation dictionary mapping the orthography to phones will be used to build the training lexicon. See attached letter_to_sound file for an example. Note that the sound symbol isn't IPA, it is just a symbol that can be used internally to uniquely identify that speech signal.







