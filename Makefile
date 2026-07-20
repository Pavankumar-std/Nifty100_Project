# ==========================================
# Nifty100 Project Makefile
# ==========================================

load:
	python src/etl/loader.py

validate:
	python src/etl/validator.py

ratios:
	python src/analytics/ratios.py

screener:
	python src/analytics/screener.py

test:
	python -m pytest

report:
	type output\validation_failures.csv

dashboard:
	echo Dashboard module coming in Sprint 2

api:
	echo API module coming in Sprint 3

clean:
	del /Q db\*.db
	del /Q output\*.csv