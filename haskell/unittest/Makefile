DOCTEST_CMD = doctest
RUN_CMD = runhaskell

doctest:
	$(DOCTEST_CMD) DocTestSample.hs

spec:
	$(RUN_CMD) SpecSample.hs

unit:
	$(RUN_CMD) UnitSample.hs

all_test: doctest spec unit
