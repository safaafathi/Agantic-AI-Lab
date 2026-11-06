# ============================================================
# Smart Student Data Analysis Agent Using Smolagents
# ============================================================

import re
import pandas as pd

from smolagents import CodeAgent, LiteLLMModel, tool
from tools import load_data


# ============================================================
# Configuration
# ============================================================

DATA_FILE = "data/students.csv"

memory = {
    "last_question": None,
    "last_result": None,
    "average_gpa": None
}


# ============================================================
# Data Loading
# ============================================================

def get_data():
    """
    Load the student dataset.
    """
    df = load_data(DATA_FILE)

    if df.empty:
        raise ValueError("The student dataset is empty.")

    required_columns = ["Name", "GPA"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Invalid dataset: missing column '{column}'."
            )

    df["GPA"] = pd.to_numeric(df["GPA"], errors="raise")

    if df["GPA"].isna().any():
        raise ValueError("The GPA column contains missing values.")

    if not df["GPA"].between(0, 4).all():
        raise ValueError(
            "Invalid dataset: GPA values must be between 0 and 4."
        )

    return df


# ============================================================
# GPA Validation
# ============================================================

def validate_gpa_threshold(gpa: float):
    """
    Validate GPA threshold.
    """
    if not 0 <= gpa <= 4:
        raise ValueError(
            "Threshold must be between 0 and 4."
        )


def validate_gpa_range(min_gpa: float, max_gpa: float):
    """
    Validate GPA range.
    """
    validate_gpa_threshold(min_gpa)
    validate_gpa_threshold(max_gpa)

    if min_gpa > max_gpa:
        raise ValueError(
            "Minimum GPA cannot be greater than maximum GPA."
        )


# ============================================================
# Question Validation
# ============================================================

def validate_question(question: str):
    """
    Validate GPA thresholds in natural-language questions.
    """

    question_lower = question.lower().strip()

    # GPA between two values
    range_match = re.search(
        r"between\s*(\d+(?:\.\d+)?)\s*"
        r"(?:and|to)\s*(\d+(?:\.\d+)?)",
        question_lower
    )

    if range_match:
        min_gpa = float(range_match.group(1))
        max_gpa = float(range_match.group(2))

        validate_gpa_range(min_gpa, max_gpa)
        return

    # GPA above or below a number
    threshold_match = re.search(
        r"\b(?:above|greater than|more than|below|less than|under)"
        r"\s*(\d+(?:\.\d+)?)",
        question_lower
    )

    if threshold_match:
        threshold = float(threshold_match.group(1))
        validate_gpa_threshold(threshold)


# ============================================================
# Tool 1: Average GPA
# ============================================================

@tool
def get_average_gpa() -> str:
    """
    Calculate the average GPA.

    Returns:
        Average GPA of all students.
    """
    df = get_data()

    average = df["GPA"].mean()

    return f"Average GPA: {average:.2f}"


# ============================================================
# Tool 2: Highest GPA Student
# ============================================================

@tool
def get_highest_gpa_student() -> str:
    """
    Find the student with the highest GPA.

    Returns:
        Name and GPA of the highest-performing student.
    """
    df = get_data()

    max_gpa = df["GPA"].max()

    students = df[df["GPA"] == max_gpa]

    names = ", ".join(
        students["Name"].astype(str).tolist()
    )

    return (
        f"Student(s) with highest GPA: "
        f"{names} ({max_gpa:.2f})"
    )


# ============================================================
# Tool 3: Students Above GPA
# ============================================================

@tool
def count_students_above_gpa(gpa: float) -> str:
    """
    Count students above a GPA threshold.

    Args:
        gpa: GPA threshold between 0 and 4.

    Returns:
        Number of students above the GPA threshold.
    """
    try:
        validate_gpa_threshold(gpa)

        df = get_data()

        count = len(df[df["GPA"] > gpa])

        return f"Students above GPA {gpa}: {count}"

    except ValueError as error:
        return f"Validation error: {error}"


# ============================================================
# Tool 4: Total Students
# ============================================================

@tool
def get_student_count() -> str:
    """
    Count all students.

    Returns:
        Total number of students.
    """
    df = get_data()

    return f"Total students: {len(df)}"


# ============================================================
# Shared Analysis Function
# ============================================================

def process_student_question(question: str) -> str:
    """
    Process supported student-data questions using Pandas.
    """

    q = question.lower().strip()

    # IMPORTANT: Validate thresholds before any calculations.
    validate_question(question)

    df = get_data()

    # --------------------------------------------------------
    # Students Above Average
    # --------------------------------------------------------

    if (
        "above average" in q
        or "above the average" in q
    ):
        average = df["GPA"].mean()

        count = len(df[df["GPA"] > average])

        return (
            f"Number of students above the average GPA "
            f"({average:.2f}): {count}"
        )

    # --------------------------------------------------------
    # Percentage Above GPA
    # --------------------------------------------------------

    if "percentage" in q or "percent" in q:
        match = re.search(
            r"\b(?:above|greater than|more than)"
            r"\s*(\d+(?:\.\d+)?)",
            q
        )

        if match:
            threshold = float(match.group(1))
            validate_gpa_threshold(threshold)

            count = len(df[df["GPA"] > threshold])
            total = len(df)

            percentage = (count / total) * 100

            return (
                f"Students above GPA {threshold}: "
                f"{count} out of {total} "
                f"({percentage:.2f}%)"
            )

    # --------------------------------------------------------
    # GPA Between Two Values
    # --------------------------------------------------------

    if "between" in q:
        match = re.search(
            r"between\s*(\d+(?:\.\d+)?)\s*"
            r"(?:and|to)\s*(\d+(?:\.\d+)?)",
            q
        )

        if match:
            min_gpa = float(match.group(1))
            max_gpa = float(match.group(2))

            validate_gpa_range(min_gpa, max_gpa)

            count = len(
                df[
                    (df["GPA"] >= min_gpa)
                    & (df["GPA"] <= max_gpa)
                ]
            )

            return (
                f"Students with GPA between "
                f"{min_gpa} and {max_gpa}: {count}"
            )

    # --------------------------------------------------------
    # Students Above GPA
    # --------------------------------------------------------

    above_match = re.search(
        r"\b(?:above|greater than|more than)"
        r"\s*(\d+(?:\.\d+)?)",
        q
    )

    if above_match:
        threshold = float(above_match.group(1))

        validate_gpa_threshold(threshold)

        count = len(df[df["GPA"] > threshold])

        return f"Students above GPA {threshold}: {count}"

    # --------------------------------------------------------
    # Students Below GPA
    # --------------------------------------------------------

    below_match = re.search(
        r"\b(?:below|less than|under)"
        r"\s*(\d+(?:\.\d+)?)",
        q
    )

    if below_match:
        threshold = float(below_match.group(1))

        validate_gpa_threshold(threshold)

        count = len(df[df["GPA"] < threshold])

        return f"Students below GPA {threshold}: {count}"

    # --------------------------------------------------------
    # Highest GPA Student
    # --------------------------------------------------------

    if (
        "highest gpa" in q
        or "who has the highest" in q
        or "best gpa" in q
        or "top student" in q
    ):
        return get_highest_gpa_student()

    # --------------------------------------------------------
    # Lowest GPA
    # --------------------------------------------------------

    if (
        "minimum gpa" in q
        or "lowest gpa" in q
        or "min gpa" in q
    ):
        return f"Minimum GPA: {df['GPA'].min():.2f}"

    # --------------------------------------------------------
    # Maximum GPA
    # --------------------------------------------------------

    if (
        "maximum gpa" in q
        or "max gpa" in q
    ):
        return f"Maximum GPA: {df['GPA'].max():.2f}"

    # --------------------------------------------------------
    # Median GPA
    # --------------------------------------------------------

    if "median" in q:
        return f"Median GPA: {df['GPA'].median():.2f}"

    # --------------------------------------------------------
    # Average GPA
    # --------------------------------------------------------

    if (
        "average gpa" in q
        or "mean gpa" in q
        or "average grade" in q
    ):
        return get_average_gpa()

    # --------------------------------------------------------
    # Dataset Columns
    # --------------------------------------------------------

    if (
        "columns" in q
        or "column names" in q
        or "features" in q
    ):
        return (
            "Dataset columns: "
            + ", ".join(df.columns.astype(str))
        )

    # --------------------------------------------------------
    # Basic Statistics
    # --------------------------------------------------------

    if (
        "statistics" in q
        or "summary" in q
    ):
        return (
            f"Total students: {len(df)}\n"
            f"Average GPA: {df['GPA'].mean():.2f}\n"
            f"Maximum GPA: {df['GPA'].max():.2f}\n"
            f"Minimum GPA: {df['GPA'].min():.2f}\n"
            f"Median GPA: {df['GPA'].median():.2f}"
        )

    # --------------------------------------------------------
    # Total Students
    # --------------------------------------------------------

    if (
        "total students" in q
        or "number of students" in q
        or "how many students" in q
        or "count students" in q
        or "students are there" in q
    ):
        return get_student_count()

    return ""


# ============================================================
# Tool 5: Analyze Student Data
# ============================================================

@tool
def analyze_student_data(operation: str) -> str:
    """
    Analyze student data using a natural-language operation.

    Args:
        operation: Student-data analysis request.

    Returns:
        The result of the requested analysis.
    """
    try:
        result = process_student_question(operation)

        if result:
            return result

        return (
            "Unsupported analysis operation. "
            "Try asking about GPA statistics, "
            "student counts, or GPA thresholds."
        )

    except ValueError as error:
        return f"Validation error: {error}"


# ============================================================
# Agent Instructions
# ============================================================

instructions = """
You are a Smart Student Data Analysis Agent.

You answer questions about student data using tools.

Rules:
1. Use the actual dataset.
2. Never invent student names or GPA values.
3. GPA thresholds must be between 0 and 4.
4. Reject invalid thresholds.
5. Explain unsupported requests.
6. Give clear and concise answers.
"""


# ============================================================
# Model Configuration
# ============================================================

model = LiteLLMModel(
    model_id="ollama/qwen2.5:1.5b",
    api_base="http://localhost:11434"
)


# ============================================================
# Create Agent
# ============================================================

agent = CodeAgent(
    tools=[
        get_average_gpa,
        get_highest_gpa_student,
        count_students_above_gpa,
        get_student_count,
        analyze_student_data
    ],
    model=model,
    max_steps=5,
    additional_authorized_imports=["pandas", "re"],
    instructions=instructions
)


# ============================================================
# Memory and Question Handling
# ============================================================

def run_with_memory(question: str) -> str:
    """
    Process a question and store the result in memory.
    """

    memory["last_question"] = question

    try:
        # Validate the question before any analysis.
        validate_question(question)

        # Handle supported questions directly.
        result = process_student_question(question)

        if not result:
            # Use the AI Agent for other questions.
            result = str(agent.run(question))

        memory["last_result"] = result

        if (
            "average gpa" in question.lower()
            or "mean gpa" in question.lower()
        ):
            memory["average_gpa"] = result

        return result

    except ValueError as error:
        result = f"Validation error: {error}"
        memory["last_result"] = result
        return result

    except Exception as error:
        result = f"Unable to process the question: {error}"
        memory["last_result"] = result
        return result


# ============================================================
# Evaluation Tests
# ============================================================

def run_evaluation_tests():
    """
    Run evaluation tests for the student-data agent.
    """

    tests = [
        {
            "name": "Average GPA",
            "question": "What is the average GPA?",
            "expected": "3.39"
        },
        {
            "name": "Highest GPA",
            "question": "Who has the highest GPA?",
            "expected": "Huda"
        },
        {
            "name": "Students above 3.5",
            "question": "How many students have GPA above 3.5?",
            "expected": "Students above GPA 3.5: 4"
        },
        {
            "name": "Students above average",
            "question": "How many students are above average GPA?",
            "expected": "6"
        },
        {
            "name": "Total students",
            "question": "How many students are there?",
            "expected": "Total students: 10"
        },
        {
            "name": "Invalid GPA above 5",
            "question": "How many students have GPA above 5?",
            "expected": "Validation error"
        },
        {
            "name": "Invalid GPA below 6",
            "question": "How many students have GPA below 6?",
            "expected": "Validation error"
        }
    ]

    passed = 0

    print("\n" + "=" * 55)
    print("SMART STUDENT DATA ANALYSIS AGENT")
    print("EVALUATION RESULTS")
    print("=" * 55)

    for test in tests:
        try:
            result = run_with_memory(test["question"])

            success = (
                test["expected"].lower()
                in str(result).lower()
            )

            if success:
                passed += 1
                status = "PASS"
            else:
                status = "FAIL"

            print(f"\nTest: {test['name']}")
            print(f"Status: {status}")
            print(f"Expected: {test['expected']}")
            print(f"Actual: {result}")

        except Exception as error:
            print(f"\nTest: {test['name']}")
            print("Status: FAIL")
            print(f"Error: {error}")

    print("\n" + "=" * 55)
    print(f"Evaluation score: {passed}/{len(tests)}")
    print("=" * 55)

    return passed, len(tests)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    run_evaluation_tests()