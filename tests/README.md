# Tests

This folder contains automated tests for the project.

How to run tests locally:

1. Activate the project's virtual environment (if any):

   source .venv/bin/activate

2. Install dev dependencies:

   pip install -r requirements.txt

3. Run pytest:

   pytest -q

Notes
- Keep tests fast and hermetic. Unit tests should not depend on a local database unless marked as integration tests.
