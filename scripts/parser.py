import re
import csv
import os
from os import listdir
from os.path import join, isfile
LOGS_PATH = "/workspace/logs"
pattern_time = re.compile("(\d*.\d*) real")
pattern_im_s = re.compile("total images/sec: (\d*.\d*)")
log_groups = {}

def readlines_reverse(filename):
    with open(filename) as qfile:
        qfile.seek(0, os.SEEK_END)
        position = qfile.tell()
        line = ''
        while position >= 0:
            qfile.seek(position)
            next_char = qfile.read(1)
            if next_char == "\n":
                yield line[::-1]
                line = ''
            else:
                line += next_char
            position -= 1
        yield line[::-1]

dirs = listdir(LOGS_PATH)
for d in dirs:
    files = [f for f in listdir(join(LOGS_PATH, d)) if isfile(join(LOGS_PATH, d, f))]
    result_time = {}
    result_im_s
    for filename in files:
        i = 0
        time = 0
        im_s = 0 
        times = []
        im_s_l = []
        for line in readlines_reverse(join(LOGS_PATH, d, filename)):
            times += pattern_time.findall(line) 
            im_s_l += pattern_im_s.findall(line)
            i=i+1
            if i >=10: break #only process 10 last lines
        if times: time = max(times)
        if im_s_l: im_s=im_s_l[0]

        filename = filename[:-4]
        result_time[filename] = time
        result_im_s[filename] = im_s
    log_groups[d] = result_time 
for key1 in log_groups.keys():
    with open('/web/csv/%s.csv'%(key1), 'w') as f:
        for key2 in sorted(log_groups[key1].keys(), key=lambda x:x[0]): #sort keys by first char (important for gpu scalability test)
            f.write("%s,%s\n"%(key2,log_groups[key1][key2]))
