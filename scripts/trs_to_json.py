import xml.etree.ElementTree as ET
import glob
import sys
import os
import argparse
import json
import platform
import uuid

parser = argparse.ArgumentParser(description='.', formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-d', '--indir', dest='inputDir', help='Input directory, default=\'.\'', default='.')
parser.add_argument('-v', '--verbose', dest='verbose', help='More logging to console.', action="store_true")

args = parser.parse_args()

g_baseDir = args.inputDir

g_verboseOutput = args.verbose

if g_verboseOutput:
    sys.stderror.write(g_baseDir + "\n")


def findFirstFileByExt(setOfAllFiles, exts):
    for f in setOfAllFiles:
        name, ext = os.path.splitext(f)
        if ("*" + ext.lower()) in exts:
            return f
    return ""


def findFilesByExt(setOfAllFiles, exts):
    res = []
    for f in setOfAllFiles:
        name, ext = os.path.splitext(f)
        if ("*" + ext.lower()) in exts:
            res.append(f)
    return res


def condLog(cond, text):
    if cond:
        # Super-annoying mumbojumbo to work around utf8 file name and the windows console which under the debugger claims to be utf8 but then fails regardless!
        if platform.system() == 'Windows':
            sys.stderr.write(text.encode('cp850', errors='backslashreplace').decode(sys.stdout.encoding))
        else:
            sys.stderr.write(text)
        sys.stderr.flush()


allFilesInDir = set(glob.glob(os.path.join(g_baseDir, "**"), recursive=True))

transcriptNames = findFilesByExt(allFilesInDir, set(["*.trs"]))


def processFile(fileName):
    condLog(g_verboseOutput, "Processing transcript '%s'\n" % fileName)

    utterances = []
    try:
        tree = ET.parse(fileName)
        root = tree.getroot()
        waveName = root.attrib['audio_filename'] + ".wav"
        turnNodes = tree.findall(".//Turn")

        for turnNode in turnNodes:
            utterances = utterances + processTurn(fileName, turnNode, waveName, tree)
    except ET.ParseError as err:
        condLog(True, "XML parser failed to parse '%s'!\n" % fileName)
        condLog(True, str(err))
    return utterances


def processTurn(fileName, turnNode, waveName, tree):

    # turnStart = float(turnNode.attrib['startTime'])
    turnEnd = float(turnNode.attrib['endTime'])
    speakerId = turnNode.get('speaker', '')

    speakerNameNode = tree.find(".//Speaker[@id='%s']" % speakerId)
    speakerName = ""
    if speakerNameNode is not None:
        speakerName = speakerNameNode.attrib['name']
    else:
        speakerName = str(uuid.uuid4())
    items = [(ch.attrib['time'], ch.tail.strip()) for ch in turnNode.findall("./Sync")]

    baseDir, name = os.path.split(fileName)
    baseName, _ = os.path.splitext(name)
    waveFileName = os.path.join(baseDir, waveName)

    result = []

    for i in range(0, len(items)):
        timeStr, transStr = items[i]
        startTime = float(timeStr)
        if i < len(items) - 1:
            timeStr2, _ = items[i + 1]
            endTime = float(timeStr2)
        else:
            endTime = turnEnd
        result.append({"speakerId": speakerName, "audioFileName": waveFileName, "transcript": transStr, "startMs": startTime * 1000.0, "stopMs": endTime * 1000.0})
        startTime = endTime
    return result


# iterate through all .trs files and process them, creates audio clip files and returns the set {fileName, transcriptString, speakerID}
utterances = []
for fn in transcriptNames:
    utterances = utterances + processFile(fn)

resultBaseName, name = os.path.split(g_baseDir)

# if name == '.':
#    outFileName = "utterances.json"
# else:
#    outFileName = name + ".json"

# with open(outFileName, 'w') as outfile:
outfile = sys.stdout
json.dump(utterances, outfile, indent=2)
