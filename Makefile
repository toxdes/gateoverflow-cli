# don't know what alternatives are there
# this is fine until I find something else
# also maybe I should use docker
default:
	python3 -m src
t:
	python3 ./src/temp.py
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
