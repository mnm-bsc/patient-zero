run:
	@echo "Running simulations..."
	python3 src/patient_zero/experiments/simulations.py
	@echo "Running experiments..."
	python3 src/patient_zero/experiments/experiments.py

clean:
	@echo "Cleaning simulations..."
	rm -rf src/patient_zero/experiments/simulations/*
	@echo "Cleaning results..."
	rm -rf src/patient_zero/experiments/results.csv