#! /usr/bin/env python3

from sys import stdin, argv, stderr
from pickle import load
from re import match

replacements = { 
    'parempansa' : ['\t"parempi" A Cmp Sg Gen Px3 abc',
                    '\t"parka" A Cmp Pl Nom Px3 abc',
                    '\t"parka" A Cmp Sg Nom Px3 abc'],
    'aiemmin' : ['\t"aiemmin" Adv Cmp abc',
                 '\t"aiempi" A Cmp Pl Ins abc',
                 '\t"aiempi" A Cmp Sg Nom abc'],
    'paremmin' : ['\t"paremmin" Adv Cmp abc',
                  '\t"parempi" A Cmp Sg Nom abc',
                  '\t"parka" A Cmp Pl Ins abc'],
    '&' : ['\t"&" Adv noabc',
           '\t"&" CC noabc'],
    'sillä' : ['\t"se" Pron Dem Sg Ade abc #1',
               '\t"sillä" CC abc #1'],
    'sekä' : ['\t"sekä" CC abc #1',
              '\t"sekä" CCM abc #1'],
    "joko" : ['\t"jo" Adv Ko abc #1',
              '\t"joko" CC abc #1',
              '\t"joko" CCM abc #1'],
    "niin" : ['\t"ne" Pron Dem Pl Ins abc #1',
              '\t"niin" Adv Dem abc #1',
              '\t"niin" Adv abc #1',
              '\t"niin" CCM abc #1'],
    "Joko" : ['\t"Jo" N Prop Sg Nom Ko Abc #1',
              '\t"jo" Adv Ko Abc #1',
              '\t"joko" CC Abc #1',
              '\t"joko" CCM Abc #1'],
    "Sekä" : ['\t"sekä" CC Abc #1',
              '\t"sekä" CCM Abc #1'],
    "Niin" : ['\t"ne" Pron Dem Pl Ins Abc #1',
              '\t"niin" Adv Abc #1',
              '\t"niin" Adv Dem Abc #1',
              '\t"niin" CCM Abc #1'],
    "ettäs" : ['\t"ettäs" Adv abc #1']
    }

def get_wf(line):
    return line[2:-2]

def replace_and_print_cohort(wf, analyses):    
    if wf == '':
        return
    elif wf in replacements:
        analyses = replacements[wf]
    elif match('.+-$', wf):    
        info_tags = analyses[0].split(' ')[-2:]
        info_str = ' '.join(info_tags) 
        lemma = wf[:-1]
        analyses = [('\t"%s" Trunc Prefix %s') % (lemma, info_str)]
    elif match('^-.+', wf):
        new_analyses = []
        for analysis in analyses:
            morph_tags = analysis.split(' ')[:-2] 
            info_tags = analysis.split(' ')[-2:]
            analysis = ' '.join(morph_tags + ['Suffix'] + info_tags)
            new_analyses.append(analysis)
        analyses = new_analyses
    elif match('^[0-9]+[.]$', wf):
        analyses = [('\t"%s" Num Ord noabc' % wf)]
    elif match('^[0-9][0-9,.]*$', wf):
        analyses = [('\t"%s" Num Card noabc' % wf)]
    elif len(analyses) > 0 and analyses[0].find("Missing ") != -1:
        info_tag = analyses[0].split(' ')[-1]
        analyses = ["\tMissing %s" % info_tag]

    print('"<%s>"' % wf)
    for line in analyses:
        print(line)

wf = ''
analyses = []

for line in stdin:
    line = line.strip('\n')

    if line == '':
        print()
    elif line[0] == '"':
        replace_and_print_cohort(wf, analyses)

        wf = get_wf(line)
        analyses = []
    else:
        analyses.append(line)

if analyses != []:    
    replace_and_print_cohort(wf, analyses)
