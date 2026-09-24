
# ============================================================
# Smart Student Data Analysis Agent
# Using Smolagents + Ollama + Qwen
# ============================================================

import re
import pandas as pd

from smolagents import CodeAgent, LiteLLMModel, tool
from tools import load_data


# ============================================================
# 1. Dataset Configuration
# ============================================================

DATA_FILE = "data/students.csv"


# ============================================================
# 2. Load Student Data
# ============================================================

def get_data():
    """
    Load the current student dataset.
    """
    return load_data(DATA_FILE)


# ============================================================
# 3. Tool: Calculate Average GPA
# ============================================================

@tool
def get_average_gpa() -> str:
    """
    Calculate the average GPA of all students.

    Returns:
        The average GPA.
    """

    df = get_data()

    average = df["GPA"].mean()

    return f"Average GPA: {average:.2f}"


# ============================================================
# 4. Tool: Find Student With Highest GPA
# ============================================================

@tool
def get_highest_gpa_student() -> str:
    """
    Find the student with the highest GPA.

    Returns:
        Student name and GPA.
    """

    df = get_data()

    max_gpa = df["GPA"].max()

    student = df[df["GPA"] == max_gpa].iloc[0]

    return (
        f"Student with highest GPA: "
        f"{student['Name']} ({student['GPA']})"
    )


# ============================================================
# 5. Tool: Count Students Above a GPA
# ============================================================

@tool
def count_students_above_gpa(gpa: float) -> str:
    """
    Count students whose GPA is greater than the given GPA.

    Args:
        gpa: GPA threshold.

    Returns:
        Number of students above the GPA.
    """

    df = get_data()

    count = len(df[df["GPA"] > gpa])

    return f"Students above GPA {gpa}: {count}"


# ============================================================
# 6. Tool: Count All Students
# ============================================================

@tool
def get_student_count() -> str:
    """
    Count the total number of students in the dataset.

    Returns:
        Total number of students.
    """

    df = get_data()

    count = len(df)

    return f"Total number of students: {count}"


# ============================================================
# 7. Main Data Analysis Tool
# ============================================================

@tool
def analyze_student_data(operation: str) -> str:
    """
    Perform a data analysis operation on the student dataset.

    Args:
        operation: The data analysis operation requested by the user,
                   such as minimum GPA, maximum GPA, median GPA,
                   average GPA, student count, columns,
                   students above or below a GPA,
                   students between GPA values,
                   percentage calculations, listing students,
                   or basic statistics.

    Returns:
        The result of the requested data analysis.
    """

    df = get_data()

    operation_lower = operation.lower().strip()

    # ========================================================
    # Total number of students
    # ========================================================

    if (
        "total student" in operation_lower
        or "student count" in operation_lower
        or "number of students" in operation_lower
        or "how many students" in operation_lower
    ):

        return f"Total number of students: {len(df)}"


    # ========================================================
    # Dataset columns
    # ========================================================

    if (
        "column" in operation_lower
        or "fields" in operation_lower
    ):

        columns = ", ".join(df.columns)

        return f"Dataset columns: {columns}"


    # ========================================================
    # Minimum GPA
    # ========================================================

    if (
        "minimum gpa" in operation_lower
        or "lowest gpa" in operation_lower
        or "min gpa" in operation_lower
    ):

        minimum = df["GPA"].min()

        return f"Minimum GPA: {minimum}"


    # ========================================================
    # Maximum GPA
    # ========================================================

    if (
        "maximum gpa" in operation_lower
        or "highest gpa" in operation_lower
        or "max gpa" in operation_lower
    ):

        maximum = df["GPA"].max()

        return f"Maximum GPA: {maximum}"


    # ========================================================
    # Median GPA
    # ========================================================

    if "median gpa" in operation_lower:

        median = df["GPA"].median()

        return f"Median GPA: {median}"


    # ========================================================
    # Average GPA
    # ========================================================

    if (
        "average gpa" in operation_lower
        or "mean gpa" in operation_lower
    ):

        average = df["GPA"].mean()

        return f"Average GPA: {average:.2f}"


    # ========================================================
    # Percentage of students above a GPA
    # Example:
    # percentage above 3
    # percentage above 3.5
    # ========================================================

    if "percentage" in operation_lower and (
        "above" in operation_lower
        or "greater than" in operation_lower
        or "more than" in operation_lower
    ):

        match = re.search(
            r"(?:above|greater than|more than)\s*(\d+(?:\.\d+)?)",
            operation_lower
        )

        if match:

            threshold = float(match.group(1))

            count = len(
                df[df["GPA"] > threshold]
            )

            total = len(df)

            percentage = (
                count / total
            ) * 100

            return (
                f"Students above GPA {threshold}: "
                f"{count} out of {total} "
                f"({percentage:.2f}%)"
            )


    # ========================================================
    # Count students above a GPA
    # Examples:
    # students above 3
    # students above 3.5
    # greater than 3
    # ========================================================

    if (
        "above" in operation_lower
        or "greater than" in operation_lower
        or "more than" in operation_lower
    ):

        match = re.search(
            r"(?:above|greater than|more than)\s*(\d+(?:\.\d+)?)",
            operation_lower
        )

        if match:

            threshold = float(match.group(1))

            count = len(
                df[df["GPA"] > threshold]
            )

            return (
                f"Students above GPA "
                f"{threshold}: {count}"
            )


    # ========================================================
    # Count students below a GPA
    # ========================================================

    if (
        "below" in operation_lower
        or "less than" in operation_lower
        or "under" in operation_lower
    ):

        match = re.search(
            r"(?:below|less than|under)\s*(\d+(?:\.\d+)?)",
            operation_lower
        )

        if match:

            threshold = float(match.group(1))

            count = len(
                df[df["GPA"] < threshold]
            )

            return (
                f"Students below GPA "
                f"{threshold}: {count}"
            )


    # ========================================================
    # Students between two GPA values
    # Example:
    # between 3 and 3.5
    # ========================================================

    if "between" in operation_lower:

        numbers = re.findall(
            r"\d+(?:\.\d+)?",
            operation_lower
        )

        if len(numbers) >= 2:

            lower = float(numbers[0])
            upper = float(numbers[1])

            count = len(
                df[
                    (df["GPA"] >= lower)
                    &
                    (df["GPA"] <= upper)
                ]
            )

            return (
                f"Students with GPA between "
                f"{lower} and {upper}: {count}"
            )


    # ========================================================
    # Students above average GPA
    # ========================================================

    if (
        "above average" in operation_lower
        or "above the average" in operation_lower
    ):

        average = df["GPA"].mean()

        count = len(
            df[df["GPA"] > average]
        )

        return (
            f"Number of students above the "
            f"average GPA ({average:.2f}): {count}"
        )


    # ========================================================
    # List all students
    # ========================================================

    if (
        "list all students" in operation_lower
        or "list students" in operation_lower
        or "show all students" in operation_lower
    ):

        return df[
            ["Student_ID", "Name", "Age",
             "Gender", "Department", "GPA"]
        ].to_string(index=False)


    # ========================================================
    # Basic statistics
    # ========================================================

    if (
        "basic statistics" in operation_lower
        or "statistics" in operation_lower
    ):

        count = len(df)

        average = df["GPA"].mean()

        minimum = df["GPA"].min()

        maximum = df["GPA"].max()

        median = df["GPA"].median()

        return (
            f"Student count: {count}\n"
            f"Average GPA: {average:.2f}\n"
            f"Minimum GPA: {minimum}\n"
            f"Maximum GPA: {maximum}\n"
            f"Median GPA: {median}"
        )


    # ========================================================
    # Unsupported operation
    # ========================================================

    return (
        "I could not identify the requested analysis. "
        "Try asking about average GPA, minimum GPA, "
        "maximum GPA, median GPA, student count, "
        "columns, students above or below a GPA, "
        "students between GPA values, percentage "
        "calculations, or basic statistics."
    )


# ============================================================
# 8. Ollama + Qwen Model
# ============================================================

model = LiteLLMModel(
    model_id="ollama/qwen2.5:1.5b",
    api_base="http://localhost:11434"
)


# ============================================================
# 9. Agent Instructions
# ============================================================

instructions = """
You are a Student Data Analysis Agent.

Your job is to answer questions about the student CSV dataset.

IMPORTANT RULES:

1. Always use the actual student dataset.

2. Never invent student names, GPA values,
   statistics, or additional data.

3. GPA values are between 0 and 4.

4. For data analysis questions, use the
   analyze_student_data tool.

5. Never create fake students or fake datasets.

6. Never use random data.

7. Never invent columns that do not exist.

8. Do not invent variables or tools.

9. If a tool returns a result, use that result directly.

10. Do not perform calculations using textual tool outputs
    when the calculation can be performed directly by
    the analyze_student_data tool.

11. If the requested information cannot be obtained
    from the dataset, clearly say so.

12. Give a clear and concise final answer.
"""


# ============================================================
# 10. Create CodeAgent
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
# 11. Conversation Memory
# ============================================================

memory = {
    "last_question": None,
    "last_result": None,
    "average_gpa": None
}


# ============================================================
# 12. Main Question Handler
# ============================================================

def run_with_memory(question: str) -> str:

    question_lower = question.lower().strip()

    memory["last_question"] = question


    # ========================================================
    # Above Average GPA
    # ========================================================

    if (
        "above average" in question_lower
        or "above the average" in question_lower
    ):

        df = get_data()

        average = df["GPA"].mean()

        count = len(
            df[df["GPA"] > average]
        )

        result = (
            f"Number of students above the "
            f"average GPA ({average:.2f}): {count}"
        )

        memory["last_result"] = result

        return result


    # ========================================================
    # Average GPA
    # ========================================================

    if (
        "average gpa" in question_lower
        or "mean gpa" in question_lower
    ):

        result = get_average_gpa()

        memory["average_gpa"] = result
        memory["last_result"] = result

        return result


    # ========================================================
    # Highest GPA
    # ========================================================

    if (
        "highest gpa" in question_lower
        or "who has the highest" in question_lower
        or "best gpa" in question_lower
    ):

        result = get_highest_gpa_student()

        memory["last_result"] = result

        return result


    # ========================================================
    # Minimum GPA
    # ========================================================

    if (
        "minimum gpa" in question_lower
        or "lowest gpa" in question_lower
        or "min gpa" in question_lower
    ):

        df = get_data()

        minimum = df["GPA"].min()

        result = f"Minimum GPA: {minimum}"

        memory["last_result"] = result

        return result


    # ========================================================
    # Maximum GPA
    # ========================================================

    if (
        "maximum gpa" in question_lower
        or "max gpa" in question_lower
    ):

        df = get_data()

        maximum = df["GPA"].max()

        result = f"Maximum GPA: {maximum}"

        memory["last_result"] = result

        return result


    # ========================================================
    # Median GPA
    # ========================================================

    if "median gpa" in question_lower:

        df = get_data()

        median = df["GPA"].median()

        result = f"Median GPA: {median}"

        memory["last_result"] = result

        return result


    # ========================================================
    # Percentage above a GPA
    # ========================================================

    if (
        "percentage" in question_lower
        and (
            "above" in question_lower
            or "greater than" in question_lower
            or "more than" in question_lower
        )
    ):

        match = re.search(
            r"(?:above|greater than|more than)\s*(\d+(?:\.\d+)?)",
            question_lower
        )

        if match:

            threshold = float(match.group(1))

            df = get_data()

            count = len(
                df[df["GPA"] > threshold]
            )

            total = len(df)

            percentage = (
                count / total
            ) * 100

            result = (
                f"Students above GPA {threshold}: "
                f"{count} out of {total} "
                f"({percentage:.2f}%)"
            )

            memory["last_result"] = result

            return result


    # ========================================================
    # Count students above a GPA
    # ========================================================

    if (
        "above" in question_lower
        or "greater than" in question_lower
        or "more than" in question_lower
    ):

        match = re.search(
            r"(?:above|greater than|more than)\s*(\d+(?:\.\d+)?)",
            question_lower
        )

        if match:

            threshold = float(match.group(1))

            result = count_students_above_gpa(
                threshold
            )

            memory["last_result"] = result

            return result


    # ========================================================
    # Count students below a GPA
    # ========================================================

    if (
        "below" in question_lower
        or "less than" in question_lower
        or "under" in question_lower
    ):

        match = re.search(
            r"(?:below|less than|under)\s*(\d+(?:\.\d+)?)",
            question_lower
        )

        if match:

            threshold = float(match.group(1))

            df = get_data()

            count = len(
                df[df["GPA"] < threshold]
            )

            result = (
                f"Students below GPA "
                f"{threshold}: {count}"
            )

            memory["last_result"] = result

            return result


    # ========================================================
    # Total students
    # ========================================================

    if (
        "total students" in question_lower
        or "number of students" in question_lower
        or "how many students are there" in question_lower
        or "student count" in question_lower
    ):

        result = get_student_count()

        memory["last_result"] = result

        return result


    # ========================================================
    # Dataset columns
    # ========================================================

    if (
        "what columns" in question_lower
        or "columns in the dataset" in question_lower
        or "dataset columns" in question_lower
    ):

        df = get_data()

        columns = ", ".join(df.columns)

        result = f"Dataset columns: {columns}"

        memory["last_result"] = result

        return result


    # ========================================================
    # Basic statistics
    # ========================================================

    if (
        "basic statistics" in question_lower
        or "statistics about the dataset" in question_lower
    ):

        df = get_data()

        count = len(df)

        average = df["GPA"].mean()

        minimum = df["GPA"].min()

        maximum = df["GPA"].max()

        median = df["GPA"].median()

        result = (
            f"Student count: {count}\n"
            f"Average GPA: {average:.2f}\n"
            f"Minimum GPA: {minimum}\n"
            f"Maximum GPA: {maximum}\n"
            f"Median GPA: {median}"
        )

        memory["last_result"] = result

        return result


    # ========================================================
    # Other questions → LLM Agent
    # ========================================================

    result = agent.run(question)

    memory["last_result"] = result

    return result


# ============================================================
# 13. Evaluation Tests
# ============================================================

def run_evaluation_tests():

    tests = [

        (
            "What is the average GPA?",
            "Average GPA: 3.39"
        ),

        (
            "Who has the highest GPA?",
            "Huda"
        ),

        (
            "How many students have GPA above 3.5?",
            "4"
        ),

        (
            "How many students are above the average GPA?",
            "6"
        ),

        (
            "How many students are there?",
            "10"
        )
    ]


    passed = 0


    print("\n")
    print("=" * 60)
    print("EVALUATION TESTS")
    print("=" * 60)


    for question, expected in tests:

        print("\nQuestion:", question)

        result = run_with_memory(question)

        print("Result:", result)

        if expected.lower() in str(result).lower():

            print("PASS")

            passed += 1

        else:

            print("FAIL")


    print("\n")
    print("=" * 60)

    print(
        f"Evaluation result: "
        f"{passed}/{len(tests)}"
    )

    if passed == len(tests):

        print("All evaluation tests passed.")

    else:

        print("Some evaluation tests failed.")

    print("=" * 60)

