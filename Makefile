.PHONY: setup data eda model plot clean

setup:
	python -m venv .venv && . .venv/bin/activate && python -m pip install -U pip && pip install -r requirements.txt
	@mkdir -p data/raw artifacts

# Usage: make data DATASET=spscientist/students-performance-in-exams
data:
	. .venv/bin/activate && python -m src.download_data $(DATASET)

eda:
	. .venv/bin/activate && python -m src.eda

model:
	. .venv/bin/activate && python -m src.model

plot:
	. .venv/bin/activate && python -m src.plot

clean:
	rm -rf data/raw/* artifacts/*

format:
	python -m black src

lint:
	python -m flake8 src
