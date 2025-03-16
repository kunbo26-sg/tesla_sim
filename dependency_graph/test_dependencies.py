import sqlite3
import pytest


# use SQLite for testing
@pytest.fixture
def db_connection():
    """Create an in-memory SQLite database with test tables."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create tables to dump test data
    cursor.execute(
        """
        CREATE TABLE dependency_rules (
            UNIT_NBR INTEGER,
            RULE_ID INTEGER,
            STEP_SEQ_ID INTEGER,
            STEP_DEP_ID INTEGER
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE prognames (
            UNIT_NBR INTEGER,
            STEP_SEQ_ID INTEGER,
            STEP_PROG_NAME TEXT
        )
    """
    )

    yield conn

    conn.close()


# SQL qeury to output the dependency
SQL_QUERY = """
WITH RECURSIVE dependency_order AS (
	-- Base Case: STEP_SEQ_ID with no Dependencies
    -- path is defined to keep track of cyclical/unlinked programs if the current step depends on a step seen before
    SELECT UNIT_NBR, STEP_SEQ_ID, 0 AS level, ',' || CAST(STEP_SEQ_ID AS TEXT) || ',' AS path
    FROM dependency_rules dr 
    WHERE UNIT_NBR = ? AND STEP_DEP_ID = 0
    
    UNION ALL
	-- recrusive Case: STEP_SEQ_ID with Dependencies
    -- path is defined to keep track of cyclical/unlinked programs if the current step depends on a step seen before
    SELECT dr.UNIT_NBR, dr.STEP_SEQ_ID, do.level + 1, do.path || CAST(dr.STEP_SEQ_ID AS TEXT) || ','
    FROM dependency_rules dr
    JOIN dependency_order do ON dr.STEP_DEP_ID = do.STEP_SEQ_ID
    
    WHERE dr.UNIT_NBR = ? AND do.path NOT LIKE '%,' || CAST(dr.STEP_SEQ_ID AS TEXT) || ',%'
),

-- Keep track of the max level depended on by each STEP
max_dependency_level AS (
    SELECT UNIT_NBR, STEP_SEQ_ID, MAX(level) AS level
    FROM dependency_order
    GROUP BY UNIT_NBR, STEP_SEQ_ID
)

-- Join the progname 
SELECT ml.level, pn.STEP_PROG_NAME
FROM max_dependency_level ml
JOIN prognames pn ON ml.UNIT_NBR = pn.UNIT_NBR AND ml.STEP_SEQ_ID = pn.STEP_SEQ_ID
ORDER BY ml.level, ml.STEP_SEQ_ID;
"""


# Unit Tests


def test_normal_dependency_chain(db_connection):
    """Test the example given (1 -> 2 -> (3,4) -> 5)."""
    cursor = db_connection.cursor()

    # Insert test data
    cursor.executemany(
        "INSERT INTO prognames VALUES (?, ?, ?)",
        [
            (1, 1, "Program1"),
            (1, 2, "Program2"),
            (1, 3, "Program3"),
            (1, 4, "Program4"),
            (1, 5, "Program5"),
        ],
    )
    cursor.executemany(
        "INSERT INTO dependency_rules VALUES (?, ?, ?, ?)",
        [
            (1, 1, 1, 0),  # Base Case
            (1, 2, 2, 1),
            (1, 3, 3, 2),
            (1, 4, 4, 2),
            (1, 5, 5, 3),  # 5 depends on 3
            (1, 6, 5, 4),  # 5 depends on 4
        ],
    )
    db_connection.commit()

    # Execute the SQL query with progname 1
    cursor.execute(SQL_QUERY, (1, 1))
    results = cursor.fetchall()

    expected = [
        (0, "Program1"),
        (1, "Program2"),
        (2, "Program3"),
        (2, "Program4"),
        (3, "Program5"),
    ]

    assert results == expected


def test_no_dependencies(db_connection):
    """Test a case with no dependencies (all steps independent)."""
    cursor = db_connection.cursor()

    # Insert test data
    cursor.executemany(
        "INSERT INTO prognames VALUES (?, ?, ?)",
        [
            (1, 1, "Program1"),
            (1, 2, "Program2"),
            (1, 3, "Program3"),
        ],
    )
    cursor.executemany(
        "INSERT INTO dependency_rules VALUES (?, ?, ?, ?)",
        [
            (1, 1, 1, 0),
            (1, 2, 2, 0),
            (1, 3, 3, 0),
        ],
    )
    db_connection.commit()

    # Execute the SQL query with progname 1
    cursor.execute(SQL_QUERY, (1, 1))
    results = cursor.fetchall()

    expected = [
        (0, "Program1"),
        (0, "Program2"),
        (0, "Program3"),
    ]

    assert results == expected


def test_circular_dependency(db_connection):
    """Test handling of circular dependencies (1 -> 2 -> 1)."""
    cursor = db_connection.cursor()

    # Insert test data with a cycle
    cursor.executemany(
        "INSERT INTO prognames VALUES (?, ?, ?)",
        [
            (1, 1, "Program1"),
            (1, 2, "Program2"),
        ],
    )
    cursor.executemany(
        "INSERT INTO dependency_rules VALUES (?, ?, ?, ?)",
        [
            (1, 1, 1, 0),
            (1, 2, 2, 1),
            (1, 3, 1, 2),  # 1 again depends on 2, cyclical
        ],
    )
    db_connection.commit()

    # Execute the SQL query should handle cycle by excluding cyclic paths
    cursor.execute(SQL_QUERY, (1, 1))
    results = cursor.fetchall()

    # Cycle only goes up to 2
    expected = [
        (0, "Program1"),
        (1, "Program2"),
    ]

    assert results == expected


def test_unlinked_steps(db_connection):
    """Test handling of steps not reachable from root)."""
    cursor = db_connection.cursor()

    # Insert test data with an unlinked step
    cursor.executemany(
        "INSERT INTO prognames VALUES (?, ?, ?)",
        [
            (1, 1, "Program1"),
            (1, 2, "Program2"),
            (1, 3, "Program3"),  # No dependencies to reach
        ],
    )
    cursor.executemany(
        "INSERT INTO dependency_rules VALUES (?, ?, ?, ?)",
        [
            (1, 1, 1, 0),
            (1, 2, 2, 1),
        ],
    )
    db_connection.commit()

    # Execute the SQL query
    cursor.execute(SQL_QUERY, (1, 1))
    results = cursor.fetchall()

    # returns the program without the unlinked prog
    expected = [
        (0, "Program1"),
        (1, "Program2"),
    ]

    assert results == expected


def test_missing_unit(db_connection):
    """Test handling of a unit not found in the db."""
    cursor = db_connection.cursor()

    # Insert test data for unit 1
    cursor.executemany(
        "INSERT INTO prognames VALUES (?, ?, ?)",
        [
            (1, 1, "Program1"),
        ],
    )
    cursor.executemany(
        "INSERT INTO dependency_rules VALUES (?, ?, ?, ?)",
        [
            (1, 1, 1, 0),
        ],
    )
    db_connection.commit()

    # Execute the SQL query for UNIT_NBR = 2
    cursor.execute(SQL_QUERY, (2, 2))
    results = cursor.fetchall()

    expected = []

    assert results == expected
