.PHONY: install pipeline test notebook clean

install:
	pip install -r requirements.txt --break-system-packages

pipeline:
	python -m src.ingestion.pipeline

stats:
	python -m src.analysis.statistics

test:
	pytest tests/ -v

notebook:
	jupyter notebook notebooks/eda_analysis.ipynb

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
