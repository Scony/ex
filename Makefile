run:
	python3 main.py
clean:
	find . -name '*~' | xargs rm -f
	find . -name '*.orig' | xargs rm -f