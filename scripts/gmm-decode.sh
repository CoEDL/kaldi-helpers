#!/bin/bash

# Original author Joshua Meyer (2016)
# modified by CoEDLers (2018)

# USAGE:
#    $ kaldi/egs/your-model/your-model-1/gmm-decode.sh
#
#    This script is meant to demonstrate how an existing GMM-HMM
#    model and its corresponding HCLG graph, build via Kaldi,
#    can be used to decode new audio files.
#    Although this script takes no command line arguments, it assumes
#    the existance of a directory (./transcriptions) and an scp file
#    within that directory (./transcriptions/wav.scp). For more on scp
#    files, consult the official Kaldi documentation.

# INPUT:
#    transcriptions/
#        wav.scp
#
#    config/
#        mfcc.conf
#
#    experiment/
#        triphones_deldel/
#            final.mdl
#
#            graph/
#                HCLG.fst
#                words.txt

# OUTPUT:
#    transcriptions/
#        feats.ark
#        feats.scp
#        delta-feats.ark
#        lattices.ark
#        one-best.tra
#        one-best-hypothesis.txt



. ./path.sh
# make sure you include the path to the gmm bin(s)
# the following two export commands are what my path.sh script contains:
# export PATH=$PWD/utils/:$PWD/../../../src/bin:$PWD/../../../tools/openfst/bin:$PWD/../../../src/fstbin/:$PWD/../../../src/gmmbin/:$PWD/../../../src/featbin/:$PWD/../../../src/lm/:$PWD/../../../src/sgmmbin/:$PWD/../../../src/fgmmbin/:$PWD/../../../src/latbin/:$PWD/../../../src/nnet2bin/:$PWD:$PATH
# export LC_ALL=C

# AUDIO --> FEATURE VECTORS
#compute-mfcc-feats \
#    --config=conf/mfcc.conf \
#    scp:data/new/wav.scp \
#    ark,scp:data/test/feats.ark,data/test/feats.scp

steps/make_mfcc.sh --nj 1 data/test exp/make_mfcc/test mfcc

#add-deltas \
#    scp:data/test/feats.scp \
#    ark:data/test/delta-feats.ark

#add-deltas scp:mfcc/raw_mfcc_test.1.scp ark:data/test/delta-feats.ark

#add-deltas scp:data/test/feats.scp ark:data/test/delta-feats.ark

#add-deltas scp:mfcc/raw_mfcc_test.1.scp ark:data/test/delta-feats.ark

apply-cmvn --utt2spk=ark:data/test/utt2spk scp:mfcc/cmvn_test.scp scp:mfcc/raw_mfcc_test.1.scp ark:- | add-deltas ark:- ark:data/test/delta-feats.ark

# TRAINED GMM-HMM + FEATURE VECTORS --> LATTICE
gmm-latgen-faster \
    --word-symbol-table=exp/tri1/graph/words.txt \
    exp/tri1/final.mdl \
    exp/tri1/graph/HCLG.fst \
    ark:data/test/delta-feats.ark \
    ark,t:lattices.ark

# TRAINED GMM-HMM + FEATURE VECTORS --> LATTICE
#gmm-latgen-faster \
#    --word-symbol-table=exp/tri1/graph/words.txt \
#    exp/tri1/final.mdl \
#    exp/tri1/graph/HCLG.fst \
#    ark:mfcc/raw_mfcc_test.1.ark \
#    ark,t:lattices.ark

# LATTICE --> BEST PATH THROUGH LATTICE
lattice-best-path \
    --word-symbol-table=exp/tri1/graph/words.txt \
    ark:lattices.ark \
    ark,t:one-best.tra

# BEST PATH INTERGERS --> BEST PATH WORDS
utils/int2sym.pl -f 2- \
    exp/tri1/graph/words.txt \
    one-best.tra \
    > one-best-hypothesis.txt

echo ""
echo ""
echo "Reference (human-provided golden transription) / Ref"
cat data/test/text

echo ""
echo ""
echo "Machine-generated transcription / Hypothesis / Hyp"
cat one-best-hypothesis.txt

echo ""
echo ""
