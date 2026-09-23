# ============================================================
# Smart Student Data Analysis Agent
# Smolagents + Ollama + Qwen
# ============================================================

from smolagents import CodeAgent, LiteLLMModel, tool
from tools import load_data, highest_gpa


# ============================================================
# 1. Connect to Ollama + Qwen
# ============================================================

model = LiteLLMModel(
    model_id="ollama/qwen2.5:1.5b",
    api_base="http://localhost:11434"
)


# ============================================================
# 2. Agent Tools
# ============================================================

@tool
def get_average_gpa() -> float:
    """Calculate the average GPA of all students."""
    df = load_data()
    return float(df["GPA"].mean())


@tool
def get_highest_gpa_student() -> str:
    """Return the student with the highest GPA."""
    df = load_data()

    student = highest_gpa(df)

    name = student.iloc[0]["Name"]
    gpa = student.iloc[0]["GPA"]

    return f"{name}, GPA: {gpa}"


@tool
def count_students_above_gpa(threshold: float) -> int:
    """
    Count students whose GPA is above the given threshold.

    Args:
        threshold: The GPA value used as the minimum threshold.
    """
    if not isinstance(threshold, (int, float)):
        raise ValueError("Threshold must be a number.")

    if threshold < 0 or threshold > 4:
        raise ValueError("Threshold must be between 0 and 4.")

    df = load_data()

    return int((df["GPA"] > threshold).sum())

@tool
def get_student_count() -> int:
    """Return the total number of students."""

    df = load_data()

    return int(len(df))


# ============================================================
# 3. Create Smolagents CodeAgent
# ============================================================

agent = CodeAgent(
    tools=[
        get_average_gpa,
        get_highest_gpa_student,
        count_students_above_gpa,
        get_student_count
    ],
    model=model,
    max_steps=3
)


# ============================================================
# 4. Validation Functions
# ============================================================

def validate_average_gpa(value):

    if not isinstance(value, (int, float)):
        return False, "Average GPA must be a number."

    if value < 0 or value > 4:
        return False, "Average GPA must be between 0 and 4."

    return True, "Average GPA is valid."


def validate_student_count(value):

    if not isinstance(value, int):
        return False, "Student count must be an integer."

    if value < 0:
        return False, "Student count cannot be negative."

    return True, "Student count is valid."


# ============================================================
# 5. Memory
# ============================================================

memory = {
    "last_question": None,
    "last_result": None,
    "average_gpa": None
}


# ============================================================
# 6. Run Agent With Memory
# ============================================================

def run_with_memory(question):

    question_lower = question.lower().strip()


    # --------------------------------------------------------
    # Average GPA
    # --------------------------------------------------------

    if "average" in question_lower and "gpa" in question_lower:

        result = get_average_gpa()

        valid, message = validate_average_gpa(result)

        if not valid:
            return message

        memory["last_question"] = question
        memory["last_result"] = result
        memory["average_gpa"] = result

        return f"Average GPA: {result:.2f}"


    # --------------------------------------------------------
    # Highest GPA
    # --------------------------------------------------------

    if (
        "highest gpa" in question_lower
        or "highest grade" in question_lower
        or "best gpa" in question_lower
        or "student with the highest" in question_lower
    ):

        result = get_highest_gpa_student()
        memory["last_question"] = question
        memory["last_result"] = result

        return result


    # ========================================================
    # IMPORTANT:
    # GPA > 3.5 MUST COME BEFORE "HOW MANY STUDENTS"
    # ========================================================

    if (
        "above 3.5" in question_lower
        or "above 3,5" in question_lower
        or "greater than 3.5" in question_lower
        or "greater than 3,5" in question_lower
        or "gpa > 3.5" in question_lower
        or "gpa > 3,5" in question_lower
        or "gpa above 3.5" in question_lower
        or "gpa above 3,5" in question_lower
    ):

        result = count_students_above_gpa(3.5)

        memory["last_question"] = question
        memory["last_result"] = result

        return f"Students with GPA above 3.5: {result}"


    # --------------------------------------------------------
    # Students Above Average
    # --------------------------------------------------------

    if "above the average" in question_lower:

        if memory["average_gpa"] is None:

            average = get_average_gpa()

            valid, message = validate_average_gpa(average)

            if not valid:
                return message

            memory["average_gpa"] = average

        average = memory["average_gpa"]

        result = count_students_above_gpa(average)

        valid, message = validate_student_count(result)

        if not valid:
            return message

        memory["last_question"] = question
        memory["last_result"] = result

        return (
            f"Average GPA: {average:.2f}\n"
            f"Students above average GPA: {result}"
        )


    # --------------------------------------------------------
    # Total Number of Students
    # --------------------------------------------------------

    if (
        "how many students" in question_lower
        or "number of students" in question_lower
        or "student count" in question_lower
    ):

        result = get_student_count()

        valid, message = validate_student_count(result)

        if not valid:
            return message

        memory["last_question"] = question
        memory["last_result"] = result

        return f"Number of students: {result}"


    # --------------------------------------------------------
    # Other Questions → Smolagents
    # --------------------------------------------------------

    result = agent.run(question)

    memory["last_question"] = question
    memory["last_result"] = result

    return str(result)


# ============================================================
# 7. Evaluation Function
# ============================================================

def check_result(test_name, actual, expected):

    if actual == expected:

        print(f"PASS: {test_name}")

        return True

    else:

        print(f"FAIL: {test_name}")
        print(f"Expected: {expected}")
        print(f"Actual: {actual}")

        return False


# ============================================================
# 8. Evaluation & Testing
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Evaluation & Testing")
    print("=" * 50)

    passed_tests = 0


    # --------------------------------------------------------
    # Test 1: Average GPA
    # --------------------------------------------------------

    print("\nTest 1: Average GPA")

    average = get_average_gpa()

    if check_result(
        "Average GPA",
        round(average, 2),
        3.39
    ):
        passed_tests += 1


    # --------------------------------------------------------
    # Test 2: Highest GPA
    # --------------------------------------------------------

    print("\nTest 2: Highest GPA")

    highest = get_highest_gpa_student()

    if check_result(
        "Highest GPA",
        highest,
        "Huda, GPA: 3.9"
    ):
        passed_tests += 1
        # --------------------------------------------------------
    # Test 3: GPA > 3.5
    # --------------------------------------------------------

    print("\nTest 3: Students with GPA > 3.5")

    count = count_students_above_gpa(3.5)

    if check_result(
        "GPA > 3.5",
        count,
        4
    ):
        passed_tests += 1


    # --------------------------------------------------------
    # Test 4: Students Above Average
    # --------------------------------------------------------

    print("\nTest 4: Students Above Average")

    average = get_average_gpa()

    above_average = count_students_above_gpa(average)

    if check_result(
        "Students above average",
        above_average,
        6
    ):
        passed_tests += 1


    # --------------------------------------------------------
    # Test 5: Invalid GPA Threshold
    # --------------------------------------------------------

    print("\nTest 5: Invalid GPA Threshold")

    try:

        count_students_above_gpa(6)

        print("FAIL: Invalid threshold was not blocked.")

    except ValueError as e:

        print("PASS: Invalid threshold was blocked.")
        print(f"Error handled: {e}")

        passed_tests += 1


    # ========================================================
    # Evaluation Summary
    # ========================================================

    print("\n" + "=" * 50)
    print("Evaluation Summary")
    print("=" * 50)

    print(f"Passed Tests: {passed_tests}/5")

    if passed_tests == 5:

        print("All evaluation tests passed.")

    else:

        print("Some evaluation tests failed.")