init:
	pip install -r requirements.txt

test:
	pytest --cov-report=html --cov=spore_codec -v
