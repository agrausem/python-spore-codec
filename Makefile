init:
	pip install -r requirements.txt

test:
	pytest --cov=spore_codec -v
