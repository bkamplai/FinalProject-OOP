MAIN = main.py
PY = python3

# target and its dependencies followed by commands
all: check_style check_types unittest unittest_pytest clean
	@echo "All done!"

unittest:
	pytest test_FILEHERE.py

test-coverage:
	pytest --cov=titlecost --cov=calc_cost test_TITLEHERE.py --cov-report term-missing

unittest_pytest:
	pytest --hypothesis-show-statistics --hypothesis-seed=100 test_TITLEHERE.py

check_types:
	mypy --disallow-untyped-defs --strict main.py board.py game.py renderer.py solver.py space.py
	mypy --disallow-untyped-defs --strict test_TITLEHERE.py

check_style:
	flake8 board.py game.py main.py renderer.py solver.py space.py --count --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	flake8 --count --show-source --statistics .

clean:
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .coverage