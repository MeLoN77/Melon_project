check:
		pylint ./main
		flake8 ./main
		mypy ./main
