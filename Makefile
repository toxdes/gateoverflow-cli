# don't know what alternatives are there
# this is fine until I find something else
# also maybe I should use docker
default:
	python3 -m gateoverflow -d
r:
# for testing release
	python3 -m gateoverflow
t:
	python3 ./gateoverflow/temp.py

build: clean
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*
	git push origin master

build-test: clean
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	rm -rf __pycache__
	rm -rf gateoverflow/__pycache__
	rm -rf build dist


