import pandas as pd


def load_data():
    """
    Load the student dataset from the CSV file.
    """
    df = pd.read_csv("data/students.csv")
    return df


def calculate_statistics(df):
    """
    Calculate basic statistics for student GPA.
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
    Filter students based on a given condition.
    """
    return df.query(condition)