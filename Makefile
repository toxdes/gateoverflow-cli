# don't know what alternatives are there
# this is fine until I find something else
# also maybe I should use docker
default:
	python3 -m gateoverflow
t:
	python3 ./gateoverflow/temp.py
clean:
	rm -rf __pycache__
	rm -rf gateoverflow/__pycache__
