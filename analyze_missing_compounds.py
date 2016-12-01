#! /usr/bin/env python3

from sys import stdin, argv, stderr
from re import split

from libhfst import HfstInputStream

def is_missing_analysis(analyses):
    return any([a.find('Missing') >= 0 for a in analyses])

def display_cohort(wf, analyses, omorfi):
    print('"<%s>"' % wf)
    if is_missing_analysis(analyses): 
        # Abc, abc or ABC depending on casing of wf.
        info_tag = analyses[0].split(' ')[-1]

        compound_parts = split('\W+', wf)
        last_part = compound_parts[-1]
        prefix = wf[:-len(last_part)]

        last_part_analyses = omorfi.lookup(last_part)

        if len(last_part) > 0 and len(last_part_analyses) > 0:            
            for analysis, weight in last_part_analyses:
                labels = analysis.split(' ')
                tags = labels[1:] + [info_tag, 
                                     'Heur', 
                                     '#%u' % (len(compound_parts) + labels[0].count('#'))]
                new_lemma = prefix + labels[0]
                print ('\t "%s" %s' % (new_lemma, ' '.join(tags)))
        else:
            print(analyses[0])
    else:
        for a in analyses:
            print(a)

if __name__=='__main__':
    if len(argv) != 2:
        stderr.write('Usage: %s omorfi\n' % argv[0])
        exit(1)

    omorfi = HfstInputStream(argv[1]).read()

    wf = ''
    analyses = []
    
    for line in map(lambda x: x.strip('\n'), stdin):
        if line == '':
            print()
        elif line[0] == '"':
            if wf != '':
                display_cohort(wf, analyses, omorfi)
                wf = ''
                analyses = []
            wf = line[2:][:-2]
        else:
            analyses.append(line)

    display_cohort(wf, analyses, omorfi)
