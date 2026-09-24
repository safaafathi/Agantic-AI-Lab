import pandas as pd


# Current CSV file used by the Agent
CURRENT_DATA_FILE = "data/students.csv"


def set_data_file(file_path):
    global CURRENT_DATA_FILE
    CURRENT_DATA_FILE = file_path


def load_data(file_path=None):

    if file_path is None:
        file_path = CURRENT_DATA_FILE

    df = pd.read_csv(file_path)

    return df


def calculate_statistics(df) -> dict:

    statistics = {
        "count": len(df),
        "average_gpa": df["GPA"].mean(),
        "maximum_gpa": df["GPA"].max(),
        "minimum_gpa": df["GPA"].min()
    }

    return statistics


def filter_students(df, condition):

    return df.query(condition)


def count_students(df):

    return len(df)


def highest_gpa(df):

    max_gpa = df["GPA"].max()

    student = df[df["GPA"] == max_gpa]

    return student