#! /usr/bin/env python3

from sys import stdin, stderr
from collections import defaultdict
from re import sub, match

ella_lemmas = set(["rönsytiarella",
                   "tiarella",
                   "tarantella",
                   "puuhella",
                   "paella",
                   "pasteurella",
                   "salmonella",
                   "sähköhella",
                   "fortunella",
                   "hella",
                   "kolumella",
                   "kaasuhella",
                   "kanella",
                   "lavantautisalmonella",
                   "chlorella",
                   "mitella",
                   "mortadella",
                   "mozzarella"])

def get_word_shape(wf):
    wf = wf.replace('-','').replace('‐','')

    if len(wf) == 0:
        return 'noabc'

    if wf.isalpha():
        if wf.islower():
            return 'abc'
        if wf.isupper():
            return 'ABC'
        if wf[0].isupper():
            return 'Abc'
        return 'aBc'
    return 'noabc'

def fix(tag):
    # Subtag Cmp sometimes duplicated.
    tag = tag.replace('Cmp Cmp', 'Cmp')

    # Subtag Sup sometimes duplicated.
    tag = tag.replace('Sup Sup', 'Sup')

    # Subtag Abbr sometimes duplicated.
    tag = tag.replace('Abbr Abbr', 'Abbr')
        
    # Remove all derivation tags.
    tag = sub(r'\[DRV=[^\]]*]','',tag)

    return tag

def noun_lemma_found(lemma_prefix, lemmas, lemma):
    correct_lemma_candidate = lemma_prefix + 'telu'
    if lemma[-1] == 'ä':
        correct_lemma_candidate = lemma_prefix + 'tely'
    if correct_lemma_candidate in lemmas:
        return 1
    correct_lemma_candidate = lemma_prefix + 'ttelu'
    if lemma[-1] == 'ä':
        correct_lemma_candidate = lemma_prefix + 'ttely'
    if correct_lemma_candidate in lemmas:
        return 1
    return 0

wf = ''
analyses = set()
lemma_dict = defaultdict(lambda : set())
compound_lemma_dict = {}
lex_dict = defaultdict(lambda : '')
lemma_component_counts = defaultdict(lambda : 0)

for line in stdin:
    line = line.strip()

    if line == "":        
        feats = get_word_shape(wf)
        print('"<' + wf + '>"')
        for analysis in analyses:
            label = analysis[1]

            for lemma in lemma_dict[label]:
                if label in lex_dict:
                    if not ((label, lemma) in lex_dict):
                        continue

                # Filter out the incorrect verb lemma for some
                # nouns. E.g. "työskentelyni" get two lemmas
                # "työskentely" and "työskennellä" with the same
                # label. "työseknnellä" is always incorrect.
                if (match('.*ell[aä]', lemma) and 
                    'N ' in label and 
                    not 'Prop' in label):
                    if noun_lemma_found(lemma[:-5], lemma_dict[label], lemma):
                        continue
                    lemma_suffix = compound_lemma_dict[lemma].split('#')[-1]
                    if not lemma_suffix in ella_lemmas:
                        new_lemma = lemma[:-5] + 'telu'
                        if lemma[-1] == 'ä':
                            new_lemma = lemma[:-5] + 'tely'
                        lemma_component_counts[new_lemma] = lemma_component_counts[lemma]
                        lemma = new_lemma

                lem = '"' + lemma.replace('#','') + '"'

                if wf.find('-') == -1:
                    lem = lem.replace('-','')
                
                if wf.find('‐') == -1:
                    lem = lem.replace('‐','')

                lex = ""
                if (label, lemma) in lex_dict:
                    lex = lex_dict[(label, lemma)]
                    
                if label.find('+?') != -1:
                    if wf == '<<s>>':
                        tag = '<s> Sent noabc'
                    else:
                        tag = ' '.join(filter(lambda x: len(x) > 0, 
                                              ['Missing', feats]))

                else:
                    print_label = label
                    if lex != '':
                        if ' ' in label:
                            print_label = label.replace(' ', ' ' + lex + ' ',1)
                        else:
                            print_label = label + ' ' + lex
                    tag = ' '.join(filter(lambda x: len(x) > 0, 
                                          filter(lambda x: x != '', 
                                                 [lem, print_label, feats])))
                    tag += ' #' + str(lemma_component_counts[lemma])
                print("\t%s" % tag)

        analyses = set()
        lemma_dict = defaultdict(lambda : set())
        compound_lemma_dict = {}
        lex_dict = defaultdict(lambda : '')
        lemma_component_counts = defaultdict(lambda : 0)
    else:
        wf, tag = line.split('\t')        
        tag = fix(tag)

        if tag.find('+?') != -1:
            analyses.add((wf, tag))
            lemma_dict[tag].add('')
        else:
            sub_tags = tag.split(' ')
            lemma = '_'.join(sub_tags[:wf.count(' ') + 1])
            
            if lemma != '#':
                component_count = lemma.count('#') + 1
 
                # Remove duplicate dashes occurring some numeral
                # forms.
                lemma = lemma.replace('--','-')

                # Remove compound markers.
                compound_lemma_dict[lemma.replace('#','')] = lemma
                lemma = lemma.replace('#','')

                if not 'Prop' in sub_tags:
                    lemma = lemma.lower()

                if (lemma_component_counts[lemma] == 0 or 
                    lemma_component_counts[lemma] > component_count):
                    lemma_component_counts[lemma] = component_count
                    
            lex = ' '.join([x for x in sub_tags[1:] if x.find('Lex_') != -1 ])
            label = ' '.join([x for x in sub_tags[wf.count(' ') + 1:] if x.find('Lex_') == -1])

            if lex != '':
                lex_dict[(label, lemma)] = lex
                lex_dict[label] = lex

            lemma_dict[label].add(lemma)
            analyses.add((wf, label))
