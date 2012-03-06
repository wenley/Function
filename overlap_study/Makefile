
.PHONY : all clean clean-sum tidy

all:
	mkdir -p db_sums
	mkdir -p org_sums
	mkdir -p outputs
	python overlap.py -a -o all -p ./outputs/
	python overlap_summary.py -d all -p ./db_sums/ -i ./outputs/
	python overlap_summary.py -o all -p ./org_sums/ -i ./outputs/

clean: tidy clean-sum

clean-sum:
	rm -fr db_sums
	rm -fr org_sums

tidy:
	rm -fr outputs