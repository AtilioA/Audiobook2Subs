#!/usr/bin/python3.8

import argparse
import sys
from pathlib import Path
import subprocess

import nltk

AUDIO_DIR = "audio"
TXT_DIR = "txt"
SRT_DIR = "srt"


# Parse cli arguments
parser = argparse.ArgumentParser(description="Segment a .txt file.")
parser.add_argument("--language", "-l")
parser.add_argument("--input", "-i")
parser.add_argument("--output", "-o")
args = parser.parse_args()
# print(args)

# Parse args, assign to variables
language = args.language
languageCode = "fr" if args.language == "french" else "por"
inputFilepath = args.input
inputFilepathStem = Path(inputFilepath).stem

# Segment input file
sentenceTokenizer = nltk.data.load(f"tokenizers/punkt/{language}.pickle")
rawText = Path(f"{TXT_DIR}/{inputFilepath}").read_text()
segmentedSentences = sentenceTokenizer.tokenize(rawText)
print(f"Segmented '{inputFilepath}' into {len(segmentedSentences)} sentences.")

# Write segmented sentences to output file
with open(
    f"{TXT_DIR}/{inputFilepathStem}_seg.txt", "w+", encoding="utf-8",
) as segmentedTxt:
    for sentence in segmentedSentences:
        segmentedTxt.write(f"{sentence.strip()}\n")

# Call aeneas with audio and output file (segmented input file) and write to .srt file
bashCommand = f'/usr/bin/python3 -m aeneas.tools.execute_task "{AUDIO_DIR}/{inputFilepath[:-7]}.mp3" "{TXT_DIR}/{inputFilepathStem}_seg.txt" "task_language={languageCode}|is_text_type=plain|os_task_file_format=srt|task_adjust_boundary_nonspeech_min=0.500|task_adjust_boundary_nonspeech_string=REMOVE" "{SRT_DIR}/{inputFilepathStem}.srt"'
# print(bashCommand)
process = subprocess.run(bashCommand, shell=True)
