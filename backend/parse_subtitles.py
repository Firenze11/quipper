import sys
import os
import re
from datetime import timedelta


def parse_file(filepath):
    time_re = "^(\d{2}):(\d{2}):(\d{2}),(\d{3})$"
    # f_out = open("temp.csv", "a+")

    with open(filepath, "r") as f_in:
        line = f_in.readline()
        # loop until end of file
        while line:
            ind = line.rstrip("\n")
            # f_out.write(ind + ",")

            line = f_in.readline()
            time_range_strs = line.rstrip("\n").split(" --> ")
            time_range = [parse_time(t, time_re=time_re) for t in time_range_strs]
            # f_out.write(time_range[0] + "," + time_range[1] + ",")

            line = f_in.readline()
            sentence_list = []
            while line and line.rstrip("\n") != "":
                sentence_list.append(line.rstrip("\n"))
                line = f_in.readline()
            # f_out.write('"' + " ".join(sentence_list) + '"' + "/n")
            sentence = " ".join(sentence_list)

            yield (ind, time_range, sentence)
            line = f_in.readline()
    # f_out.close()


def parse_time(time_str, time_re=""):
    match = re.match(time_re, time_str)
    hour, minute, second, millisecond = (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
    )
    return timedelta(
        hours=hour, minutes=minute, seconds=second, milliseconds=millisecond
    )


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
    main()

