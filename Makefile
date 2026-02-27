run:
	python3 src/patient_zero/experiments/simulations.py
	python3 src/patient_zero/experiments/experiments.py

clean:
	rm -rf src/patient_zero/experiments/simulations/*
	rm -rf src/patient_zero/experiments/results.csv

sim:
	python3 src/patient_zero/experiments/simulations.py

exp:
	python3 src/patient_zero/experiments/experiments.py