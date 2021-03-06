#!/usr/bin/env bash


MOVIE=$1
SUBTITLES=$2

START_TIME=$3
END_TIME=$4

#OUTFILE="/data/cut.mp4"
#
#rm -f $OUTFILE

# ffmpeg \
#   -ss $START_TIME \
#   -i "$MOVIE" \
#   -vcodec libx264 -crf 27 -preset veryfast \
#   -to $END_TIME \
#   -c copy \
#   -copyts \
#   -async 1 $OUTFILE

#TMP_SRT="/data/into-the-spider-verse-${START_TIME//:}.srt"
#rm -f $TMP_SRT

# First, we must generate a version of the SRT starting at $START_TIME,
# with timestamps all appropriately moved up.  Otherwise, the next command
# will start the video at $START_TIME but look for captions starting at
# 00:00:00.  (No idea why the subtitles filter doesn't respect -ss).
#ffmpeg -itsoffset -$START_TIME -i $SUBTITLES -c copy $TMP_SRT

# Producing an mpeg with burned in subtitles:
# ffmpeg \
#   -ss $START_TIME \
#   -to $END_TIME \
#   -i "$MOVIE" \
#   -vf "subtitles=filename=$TMP_SRT" \
#   -vcodec libx264 -crf 27 -preset veryfast \
#   $OUTFILE

OUTGIF=$5
if [ -e "$OUTGIF" ]
then
  exit 0
fi

mkdir -p `dirname $OUTGIF`
mkdir -p /tmp/gifs
TMPGIF=/tmp/gifs/`basename $OUTGIF`
rm -f $TMPGIF

# As always with ffmpeg, the order of arguments is very important! -ss and
# -to must come before -i to ensure that ffmpeg does a fast seek rather than
# just playing the whole movie to $START_TIME.
ffmpeg \
  -ss $START_TIME \
  -to $END_TIME \
  -i "$MOVIE" \
  -filter_complex "[0:v] subtitles=filename=$SUBTITLES:force_style='Fontsize=36',fps=12,scale=w=600:h=-1,split [a][b];[a] palettegen=stats_mode=single [p];[b][p] paletteuse=new=1" \
  $TMPGIF

mv $TMPGIF $OUTGIF
