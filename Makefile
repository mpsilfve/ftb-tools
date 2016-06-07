current_dir = $(shell pwd)
SHELL=bash

RED="\033[0;31m"
GREEN="\033[0;32m"
NC="\033[0m"

install:
	echo "$(current_dir)/ftb_omorfi" > ftb-omorfi
	echo "$(current_dir)/ftb_omorfi_amb" > ftb-omorfi-amb
	echo "$(current_dir)/ftb_tokenize" > ftb-tokenize
	echo "$(current_dir)/ftb_omorfi_no_tok" > ftb-omorfi-no-tok
		chmod u+x ftb-omorfi ftb-tokenize ftb-omorfi-no-tok ftb-omorfi-amb
	install -t ~/bin ftb-omorfi ftb-tokenize ftb-omorfi-no-tok ftb-omorfi-amb

check:
	@for f in `ls tests/*txt`; do \
        cat $$f | ./ftb_omorfi > $$f.sys ; diff -w $$f.sys $$f.expected.out > $$f.diff ; \
        if [[ -s $$f.diff ]] ; \
           then echo -e $$f $(RED) FAILED $(NC); \
           else echo -e $$f $(GREEN) PASSED $(NC); \
        fi done
	@rm tests/*diff
	@rm tests/*sys