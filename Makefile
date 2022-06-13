wordlist:
	edictor wordlist --dataset=liusinitic/cldf/cldf-metadata.json --preprocessing=edictor/preprocessing.py --name=edictor/liusinitic --addon="chinese_characters:characters,partial_cognacy:cogids,language_dialectgroup:dialectgroup,morpheme_glosses:morphemes,comment:note"
	
cognate-set-comparison:
	python cognate-set-comparison.py
part-one:
	python cognate-set-comparison.py
part-two:
	python cross-semantic-cognate-statistics.py
cross-semantic-cognate-statistics:
	python cross-semantic-cognate-statistics.py
lexical-distances:
	python lexical-distances.py
part-three:
	python lexical-distances.py
plot-distances:
	python plot-distances.py
part-four:
	python plot-distances.py
analyze-distances:
	python analyze-distances.py
part-five:
	python analyze-distances.py
part-six:
	python export-nexus.py
nexus-export:
	python export-nexus.py
