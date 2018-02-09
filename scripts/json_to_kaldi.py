#!/usr/local/bin/python3

import argparse
import json
import os
import sys
import uuid

parser = argparse.ArgumentParser(description='Convert json from stdin to Kaldi input files (in output-folder).')
parser.add_argument('--output-folder', type=str, required=True, help='The output folder')
parser.add_argument('--no-silence-markers', action="store_true", help='The input json file')
args = parser.parse_args()

# input_json_fname = args.input_json
output_folder = args.output_folder
silence_markers = not args.no_silence_markers


# f_in = open(input_json_fname, "r")
f_in = sys.stdin

json_transcripts = json.loads(f_in.read())
f_in.close()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

class KaldiInput:
    def __init__(self, output_folder):

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        self.speakers = {}
        self.recordings = {}
        self.utterances = {}

        self.l_segments, self.l_transcripts, self.l_speakers, self.l_recordings, self.l_utt2spk, self.l_corpus = [], [], [], [], [], []

        self.f_segments = open(output_folder + "/segments", "w", encoding="utf-8")
        self.f_transcripts = open(output_folder + "/text", "w", encoding="utf-8")
        self.f_speakers = open(output_folder + "/spk2gender", "w", encoding="utf-8")
        self.f_recordings = open(output_folder + "/wav.scp", "w", encoding="utf-8")
        self.f_utt2spk = open(output_folder + "/utt2spk", "w", encoding="utf-8")
        self.f_corpus = open(output_folder + "/corpus.txt", "w", encoding="utf-8")

    def add_speaker_if_missing(self, speakerId):
        if speakerId not in self.speakers:
            # create speaker id
            self.speakers[speakerId] = str(uuid.uuid4())
            # writing gender
            self.l_speakers.append(self.speakers[speakerId] + " " + "f\n")

        return self.speakers[speakerId]

    def add_recording_if_missing(self, audioFileName):
        if audioFileName not in self.recordings:
            # create recording id
            self.recordings[audioFileName] = str(uuid.uuid4())
            self.l_recordings.append(self.recordings[audioFileName] + " " + audioFileName + "\n")

        return self.recordings[audioFileName]

    def add(self, recording_id, utterance_id, startMs, stopMs, transcript, silence_markers):
        if silence_markers:
            self.l_transcripts.append(utterance_id + " !SIL " + transcript + " !SIL\n")
        else:
            self.l_transcripts.append(utterance_id + " " + transcript + "\n")
        self.l_segments.append(utterance_id + " " + recording_id + " " + "%f %f\n" % (startMs / 1000.0, stopMs / 1000.0))
        # f_utt2spk.write(utterance_id + " " + speaker_id + "\n")
        # hack to match utterances to utterances
        self.l_utt2spk.append(utterance_id + " " + utterance_id + "\n")
        self.l_corpus.append(transcript + "\n")

    def write_and_close(self):
        self.l_segments.sort()
        self.f_segments.write("".join(self.l_segments))
        self.f_segments.close()

        self.l_transcripts.sort()
        self.f_transcripts.write("".join(self.l_transcripts))
        self.f_transcripts.close()

        self.l_speakers.sort()
        self.f_speakers.write("".join(self.l_speakers))
        self.f_speakers.close()

        self.l_recordings.sort()
        self.f_recordings.write("".join(self.l_recordings))
        self.f_recordings.close()

        self.l_utt2spk.sort()
        self.f_utt2spk.write("".join(self.l_utt2spk))
        self.f_utt2spk.close()

        self.l_corpus.sort()
        self.f_corpus.write("".join(self.l_corpus))
        self.f_corpus.close()


testing_input = KaldiInput(output_folder + "/testing")
training_input = KaldiInput(output_folder + "/training")

for i, json_transcript in enumerate(json_transcripts):
    transcript = json_transcript["transcript"]
    startMs = json_transcript["startMs"]
    stopMs = json_transcript["stopMs"]

    if "speakerId" in json_transcript:
        speakerId = json_transcript["speakerId"]
    else:
        speakerId = str(uuid.uuid4())

    audioFileName = json_transcript["audioFileName"].replace("\\", "/")



    #speaker_id = speakers[speakerId]
    #recording_id = recordings[audioFileName]
    #utterance_id = speakers[speakerId] + "-" + str(uuid.uuid4())

    if i % 10 == 0:
        # add speaker id
        speaker_id = testing_input.add_speaker_if_missing(speakerId)

        # add audioFilename
        recording_id = testing_input.add_recording_if_missing(audioFileName)

        utterance_id = speaker_id + "-" + str(uuid.uuid4())

        testing_input.add(recording_id, utterance_id, startMs, stopMs, transcript, silence_markers)
    else:
        # add speaker id
        speaker_id = training_input.add_speaker_if_missing(speakerId)

        # add audioFilename
        recording_id = training_input.add_recording_if_missing(audioFileName)

        utterance_id = speaker_id + "-" + str(uuid.uuid4())

        training_input.add(recording_id, utterance_id, startMs, stopMs, transcript, silence_markers)

testing_input.write_and_close()
training_input.write_and_close()
