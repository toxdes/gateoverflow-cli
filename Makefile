# don't know what alternatives are there
# this is fine until I find something else
# also maybe I should use docker
default:
	# debug enabled
	python3 -m gateoverflow -d
r:
	# for testing release
	python3 -m gateoverflow
t:
	# for testing temporary code
	python3 ./gateoverflow/temp.py
vd:
	# version check with debug on
	python3 -m gateoverflow -d -v

v:
	# version check without debug
	python3 -m gateoverflow -v


build: clean git
	# build pypi package and upload it
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

git:
	# push code to github
	git push origin master develop

build-test: clean
	# upload to test.pypi.org repo
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	rm -rf __pycache__
	rm -rf gateoverflow/__pycache__
	rm -rf build dist


