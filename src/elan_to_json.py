#!/usr/bin/python3

"""
Get all files in the repository can use recursive atm as long as we don't need numpy
pass in corpus path throw an error if matching file wav isn"t found in the corpus directory

Usage 
"""

import glob
import sys
import os
import argparse
from pympi.Elan import Eaf
from typing import List
from pyparsing import ParseException
from src.utilities import find_files_by_extension
from src.utilities import write_data_to_json_file


def read_eaf(input_elan_file, tier_name: str) -> List[dict]:
    """
    Method to process a particular tier in an eaf file (ELAN Annotation Format). It stores the transcriptions in the 
    following format:
                    {'speaker_id': <speaker_id>,
                    'audio_file_name': <file_name>,
                    'transcript': <transcription_label>,
                    'start_ms': <start_time_in_milliseconds>,
                    'stop_ms': <stop_time_in_milliseconds>}
    :param input_elan_file: 
    :param tier_name: 
    :return: 
    """
    # Get paths to files
    input_directory, full_file_name = os.path.split(input_elan_file)
    file_name, extension = os.path.splitext(full_file_name)

    input_eaf = Eaf(input_elan_file)

    # Look for wav file matching the eaf file in same directory
    if os.path.isfile(os.path.join(input_directory, file_name + ".wav")):
        print("WAV file found for " + file_name, file=sys.stderr)
    else:
        raise ValueError(f"WAV file not found for {full_file_name}. "
                         f"Please put it next to the eaf file in {input_directory}.")

    # Get annotations and parameters (things like speaker id) on the target tier
    annotations = sorted(input_eaf.get_annotation_data_for_tier(tier_name))
    parameters = input_eaf.get_parameters_for_tier(tier_name)
    speaker_id = parameters.get("PARTICIPANT", default="")

    annotations_data = []

    for annotation in annotations:
        start = annotation[0]
        end = annotation[1]
        annotation = annotation[2]

        # print("processing annotation: " + annotation, start, end)
        obj = {
            "audio_file_name": f"{file_name}.wav",
            "transcript": annotation,
            "start_ms": start,
            "stop_ms": end
        }
        if "PARTICIPANT" in parameters:
            obj["speaker_id"] = speaker_id
        annotations_data.append(obj)

    return annotations_data


def main():

    """ Run the entire elan_to_json.py as a command line utility """

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
                            description="This script takes an directory with ELAN files and "
                                        "slices the audio and output text in a format ready "
                                        "for our Kaldi pipeline.")
    parser.add_argument("-i", "--input_dir", help="Directory of dirty audio and eaf files", default="input/data/")
    parser.add_argument("-o", "--output_dir", help="Output directory", default="../input/output/tmp/")
    parser.add_argument("-t", "--tier", help="Target language tier name", default="Phrase")
    parser.add_argument("-j", "--output_json", help="File name to output json", default="../input/output/tmp/dirty.json")
    arguments: argparse.Namespace = parser.parse_args()

    # Build output directory if needed
    if not os.path.exists(arguments.output_dir):
        os.makedirs(arguments.output_dir)

    all_files_in_directory = set(glob.glob(os.path.join(arguments.input_dir, "**"), recursive=True))
    input_eafs_files = find_files_by_extension(all_files_in_directory, {"*.eaf"})

    annotations_data = []

    for input_eaf_file in input_eafs_files:
        annotations_data.extend(read_eaf(input_eaf_file, arguments.tier))

    write_data_to_json_file(annotations_data, arguments.output_json)


if __name__ == "__main__":
    main()
