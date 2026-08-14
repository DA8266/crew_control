import pandas as pd
from main import addEmp, filter_data


# --- addEmp Tests ---

def test_add_employee_to_empty_df():
    """Tests that addEmp initializes the first employee with ID 100 on an empty DataFrame."""
    empty_df = pd.DataFrame()
    updated_df = addEmp(
        empty_df, "Jane", "Doe", 30, 70000, "HR", "2026-01-01"
    )

    assert len(updated_df) == 1
    assert updated_df.iloc[0]['emp_id'] == 100
    assert updated_df.iloc[0]['status'] == "Active"


def test_add_employee_increments_id():
    """Tests that addEmp correctly appends a row and increments the max ID."""
    df = pd.DataFrame({
        'emp_id': [100],
        'first_n': ['Alice'],
        'last_n': ['Smith'],
        'age': [29],
    })

    updated_df = addEmp(df, "John", "Doe", 40, 65000, "IT", "2026-01-05")

    assert len(updated_df) == 2
    assert updated_df.iloc[1]['first_n'] == "John"
    assert updated_df.iloc[1]['emp_id'] == 101


# --- filter_data Tests ---

def test_filter_data_contains():
    """Tests that filter_data successfully filters text using string matching."""
    df = pd.DataFrame({
        'emp_id': [100, 101],
        'first_n': ['Alice', 'Bob'],
        'last_n': ['Smith', 'Jones'],
    })

    filtered_df = filter_data(df, 'first_n', 'Alice')

    assert len(filtered_df) == 1
    assert filtered_df.iloc[0]['last_n'] == "Smith"

def test_filter_data_no_match():
    """Tests that filter_data returns an empty DataFrame if no match is found."""
    df = pd.DataFrame({'emp_id': [100], 'first_n': ['Alice']})

    filtered_df = filter_data(df, 'first_n', 'Bob')
    assert filtered_df.empty

def test_filter_data_numeric_operators():
    """Tests numeric filtering using math operators (>, <=, =)."""
    df = pd.DataFrame({
        'emp_id': [100, 101, 102],
        'first_n': ['Alice', 'Bob', 'Charlie'],
        'salary': [50000, 75000, 100000],
    })

    # Test greater than
    gt_df = filter_data(df, 'salary', 60000, operator=">")
    assert len(gt_df) == 2

    # Test equal to
    eq_df = filter_data(df, 'salary', 75000, operator="=")
    assert len(eq_df) == 1
    assert eq_df.iloc[0]['first_n'] == "Bob"

    # Test less than or equal to
    lte_df = filter_data(df, 'salary', 75000, operator="<=")
    assert len(lte_df) == 2


def test_filter_data_invalid_column():
    """Tests that filter_data safely returns an empty DataFrame when passed a non-existent column."""
    df = pd.DataFrame({'emp_id': [100], 'first_n': ['Alice']})

    filtered_df = filter_data(df, 'non_existent_column', 'Alice')
    assert filtered_df.empty


def test_filter_data_non_numeric_error_handling():
    """Tests that passing non-numeric text to numeric operators fails gracefully."""
    df = pd.DataFrame({
        'emp_id': [100],
        'first_n': ['Alice'],
        'dept': ['Engineering'],
    })

    # Department cannot be compared using math operators
    filtered_df = filter_data(df, 'dept', 'invalid_number', operator=">")
    assert filtered_df.empty