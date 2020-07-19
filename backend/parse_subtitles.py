import sys
import os
import re
from datetime import timedelta


def parse_file(filepath):
    # f_out = open("temp.csv", "a+")

    with open(filepath, "r") as f_in:
        line = f_in.readline()
        # loop until end of file
        while line:
            ind = line.rstrip("\n")
            # f_out.write(ind + ",")

            line = f_in.readline()
            time_range_strs = line.rstrip().split(" --> ")
            time_range = [parse_time(t) for t in time_range_strs]
            # f_out.write(time_range[0] + "," + time_range[1] + ",")

            line = f_in.readline()
            sentence_list = []
            while line and line.rstrip() != "":
                sentence_list.append(line.rstrip("\n"))
                line = f_in.readline()
            # f_out.write('"' + " ".join(sentence_list) + '"' + "/n")
            sentence = " ".join(sentence_list)

            yield (ind, time_range, sentence)
            line = f_in.readline()
    # f_out.close()



def write_srt_file(filepath, subtitles):
    with open(filepath, "w") as fp:
        for (idx, time_range, text) in subtitles:
            fp.write(str(idx))
            fp.write('\n')
            fp.write(format_time(time_range[0]))
            fp.write(' --> ')
            fp.write(format_time(time_range[1]))
            fp.write('\n')
            fp.write(text)
            fp.write('\n\n')

RE_TIME = "^(\d{2}):(\d{2}):(\d{2}),(\d{3})$"

def parse_time(time_str):
    match = re.match(RE_TIME, time_str)
    hour, minute, second, millisecond = (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
    )
    return timedelta(
        hours=hour, minutes=minute, seconds=second, milliseconds=millisecond
    )

def format_time(td):
    res = str(td)
    if '.' in res:
        res = res[0:-3].replace('.', ',')
    else:
        res += ',000'
    return res

def start_subs_at(orig_srt_filepath, trunc_srt_filepath, start_at):
    orig_subs = parse_file(orig_srt_filepath)
    trunc_subs = []
    idx = 1
    for sub in orig_subs:
        new_start = sub[1][0] - start_at
        new_end = sub[1][1] - start_at
        if new_start.total_seconds() >= 0:
            trunc_subs.append((idx, [new_start, new_end], sub[2]))
            idx += 1
    write_srt_file(trunc_srt_filepath, trunc_subs)

def main():
    # filepath = sys.argv[1]
    # if not os.path.isfile(filepath):
    #     print("File path {} does not exist. Exiting...".format(filepath))
    #     sys.exit()
    filepath = "/Users/lezhili/work/quipper/data/Spider-Man.Into.the.Spider-Verse.2018.720p.BluRay.x264-SPARKS.srt"
    cnt = 0
    for record in parse_file(filepath):
        print(record)
        cnt += 1
        if cnt > 100:
            break


if __name__ == "__main__":
    start_subs_at(
        "/Users/noah/quipper/data/Spider-Man.Into.The.Spider-Verse.srt",
        "/Users/noah/quipper/data/bleh.srt",
        timedelta(hours=0, minutes=2, seconds=28, milliseconds=162))

