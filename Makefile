all:
	python csv_preliminary_eval.py TURKIYE.csv > turkey_results.txt
	python csv_preliminary_eval.py ANKARA.csv > ankara_results.txt
