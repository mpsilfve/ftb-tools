current_dir = $(shell pwd)

install:
	echo "$(current_dir)/ftb_omorfi" > ftb-omorfi
	echo "$(current_dir)/ftb_omorfi_amb" > ftb-omorfi-amb
	echo "$(current_dir)/ftb_tokenize" > ftb-tokenize
	echo "$(current_dir)/ftb_omorfi_no_tok" > ftb-omorfi-no-tok
		chmod u+x ftb-omorfi ftb-tokenize ftb-omorfi-no-tok ftb-omorfi-amb
	install -t ~/bin ftb-omorfi ftb-tokenize ftb-omorfi-no-tok ftb-omorfi-amb