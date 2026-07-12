.PHONY: surrogate geometry test check status demo-gate

surrogate:
	PYTHONPATH=src python src/mft_d1600/run_surrogate.py

geometry:
	python scripts/render_geometry.py

test:
	PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'

check: geometry surrogate test
	python scripts/check_repo.py

status:
	python scripts/status.py

demo-gate:
	python scripts/demo_gate.py
