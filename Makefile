wordlist:
	edictor wordlist --dataset=liusinitic/cldf/cldf-metadata.json --preprocessing=edictor/preprocessing.py --name=edictor/liusinitic --addon=chinese_characters:characters,partial_cognacy:cogids,morpheme_glosses:morphemes,comment:note
cognate-set-comparison:
	python cognate-set-comparison.py
part-one:
	python cognate-set-comparison.py
part-two:
	python cross-semantic-cognate-statistics.py
cross-semantic-cognate-statistics:
	python cross-semantic-cognate-statistics.py
