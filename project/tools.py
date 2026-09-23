import pandas as pd


# Current CSV file used by the Agent
CURRENT_DATA_FILE = "data/students.csv"


def set_data_file(file_path):
    """
    Set the CSV file that will be used by the Agent.

    Args:
        file_path: Path to the uploaded CSV file.
    """
    global CURRENT_DATA_FILE
    CURRENT_DATA_FILE = file_path


def load_data(file_path=None):
    """
    Load the student dataset from a CSV file.

    Args:
        file_path: Optional path to the CSV file.

    Returns:
        Pandas DataFrame containing student data.
    """
    if file_path is None:
        file_path = CURRENT_DATA_FILE

    df = pd.read_csv(file_path)
    return df


def calculate_statistics(df) -> dict:
    """
    Calculate basic statistics for the student dataset.

    Args:
        df: Pandas DataFrame containing student data.

    Returns:
        Dictionary containing count, average, maximum, and minimum GPA.
    """
    statistics = {
        "count": len(df),
        "average_gpa": df["GPA"].mean(),
        "maximum_gpa": df["GPA"].max(),
        "minimum_gpa": df["GPA"].min()
    }

    return statistics


def filter_students(df, condition):
    """
    Filter students according to a condition.

    Args:
        df: Pandas DataFrame containing student data.
        condition: Pandas query condition.

    Returns:
        Filtered DataFrame.
    """
    return df.query(condition)


def count_students(df):
    """
    Count the number of students.

    Args:
        df: Pandas DataFrame containing student data.

    Returns:
        Number of students.
    """
    return len(df)


def highest_gpa(df):
    """
    Find the student with the highest GPA.

    Args:
        df: Pandas DataFrame containing student data.

    Returns:
        DataFrame containing the student with the highest GPA.
    """
    max_gpa = df["GPA"].max()
    student = df[df["GPA"] == max_gpa]

    return student