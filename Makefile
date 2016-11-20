.PHONY: runtests runapp clean
runtests:
	cd tests && nosetests -a will_run test_prog_tf.py


runapp:
	python cc_params/prog_tf.py

clean:
	cd cc_params && rm -f *.pyc
	cd tests && rm -f *.pyc

