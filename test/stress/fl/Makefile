test:
	fl-run-test test.py
	fl-run-bench test.py HttpTest.test_http
	fl-build-report --html -o _build/ bench.xml

clean:
	rm -f *.xml*
	rm -f *.log
	rm -rf _build
	rm -f *.pyc
