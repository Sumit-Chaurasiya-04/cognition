.PHONY: setup run test lint clean

setup:
	python3 -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"
	@echo "Then run: pip install -r requirements.txt"

install:
	pip install -r requirements.txt

run:
	streamlit run app/main.py

test:
	pytest tests/

lint:
	# Stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings.
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf app/__pycache__
	rm -rf tests/__pycache__