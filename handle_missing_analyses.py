#! /usr/bin/env python3

from sys import stdin

def print_res(wf, cohort):
    if wf != '':
        if len(cohort) == 1 and cohort[0][:9] == '\tMissing ':
            wf = wf + ' ' + cohort[0].strip()
            cohort = []
        print(wf)
        for e in cohort:
            print(e)

if __name__=='__main__':
    wf = ''
    cohort = []

    for line in map(lambda x: x.strip('\n'), stdin):
        if line == '':
            print(line)
        elif line[0] == '"':
            print_res(wf, cohort)
            wf = line
            cohort = []
        else:
            cohort.append(line)
    if wf != '':
        print_res(wf, cohort)
