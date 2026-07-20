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
	python src/screener/engine.py

peer:
	python src/analytics/peer.py

test:
	python -m pytest

report:
	type output\validation_failures.csv

dashboard:
	echo Dashboard module coming in future sprint

clean:
	del /Q db\*.db
	del /Q output\*.csv