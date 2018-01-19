#!/usr/bin/python3

""" Given a json file with transcript information this tools can perform 
manipulations including generating word lists.
Optionally provide the output json file name with -j

Usage: python filter_text.py sample.json wordlist.txt 
"""

import argparse
import json
import string
import os
import re
import sys


def save_wordlist(wordlist):
        """ Given a list of strings write to file
        """
        try:
                for word in wordlist: sys.stdout.write(word + '\n')
        except:
                print("Could not write out to file " + filename)
                exit()


def extract_wordlist(data):
        """ Given the data object produce a list of strings of single words
                Returned list is of unique words and sorted
        """ 
        result = []
        for utt in data:
                words = utt.get('transcript').split()
                result.extend(words)
        result = list(set(result))
        result.sort()
        return result

def load_file(filename=""):
        """ Given a filename load and return the object
        """
        try:
                f = sys.stdin
                if filename:
                        f = open(filename, "r", encoding = "utf-8")
                data = json.load(f)
        except Exception as e:
                print("Could not read file " + filename)
                exit()
        return data


def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("--infile", type=str,
                help="The input file to clean.")
        args = parser.parse_args()

        if args.infile: data = load_file(args.infile)
        else: data = load_file()

        print("Wordlist...", end='', flush=True,file=sys.stderr)
        wordlist = extract_wordlist(data)
        print("Done.",file=sys.stderr)

        print("Write out wordlist...", end='', flush=True,file=sys.stderr)
        save_wordlist(wordlist)
        print("Done.",file=sys.stderr)




if __name__ == '__main__':
        main()
