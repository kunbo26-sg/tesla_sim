# SQL Dependency Test

This project implements an SQL-based solution to determine the execution order of program steps based on dependency rules for a given `UNIT_NBR`. It uses SQLite for in-memory testing and follows test-driven development principles as outlined in the requirements.

## Features

A pytest suite to return the list of programs in order of execution handling dependencies.

Primary use

- **Dependency Resolution**: Uses a recursive CTE to compute the execution order of program steps based on dependencies.

Edge cases

- **Cycle Detection**: Handles circular dependencies by tracking visited steps in the recursion path.
- **Unlinked Steps**: Excludes steps not reachable from the dependency chain.

## Prerequisites

- Python 3.11 or higher
- Dependencies listed in `requirements.txt` (only `pytest` for testing)

## How to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kunbo26-sg/tesla_sim
   cd dependency_graph
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Tests**:
   ```bash
   pytest test_dependencies.py
   ```

## Potential Gaps

1. Depending on the size of tables, an in memory solution might not be possible to spin up.

2. Possibly in the Cyclical,Unlinked steps the failure mode should be silent instead of returning a parital solution
