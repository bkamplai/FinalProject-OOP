MAIN = main.py
TESTS = Tests/test_space.py Tests/test_board.py Tests/test_game.py Tests/test_initializingstate.py Tests/test_playingstate.py Tests/test_state.py Tests/test_solver.py Tests/test_renderer.py
PY = python3

# target and its dependencies followed by commands
all: check_style check_types unittest unittest_pytest clean
	@echo "All done!"

unittest:
	pytest -vv --hypothesis-show-statistics --hypothesis-seed=100 --cov --cov-report term-missing $(TESTS)

test-coverage:
	pytest --cov $(TESTS) --cov-report term-missing

unittest_pytest:
	pytest -v --hypothesis-show-statistics --hypothesis-seed=100 --cov --cov-report term $(TESTS)

check_types:
	mypy --disallow-untyped-defs --strict main.py board.py game.py renderer.py solver.py space.py
	mypy --disallow-untyped-defs --strict $(TESTS)

check_style:
	flake8 board.py game.py main.py renderer.py solver.py space.py --count --show-source --statistics
	flake8 $(TESTS) --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	flake8 --count --show-source --statistics .

clean:
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .coverage