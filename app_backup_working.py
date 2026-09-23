import pandas as pd
import gradio as gr


# ============================================================
# Current CSV file used by the Agent
# ============================================================

CURRENT_DATA_FILE = "data/students.csv"


# ============================================================
# Set the CSV file
# ============================================================

def set_data_file(file_path):
    """
    Set the CSV file that will be used by the Agent.
    """
    global CURRENT_DATA_FILE
    CURRENT_DATA_FILE = file_path


# ============================================================
# Load student data
# ============================================================

def load_data(file_path=None):
    """
    Load the student dataset from a CSV file.
    """
    if file_path is None:
        file_path = CURRENT_DATA_FILE

    df = pd.read_csv(file_path)
    return df


# ============================================================
# Calculate statistics
# ============================================================

def calculate_statistics(df) -> dict:
    """
    Calculate basic statistics for the student dataset.
    """

    statistics = {
        "count": len(df),
        "average_gpa": df["GPA"].mean(),
        "maximum_gpa": df["GPA"].max(),
        "minimum_gpa": df["GPA"].min()
    }

    return statistics


# ============================================================
# Filter students
# ============================================================

def filter_students(df, condition):
    """
    Filter students according to a condition.
    """

    return df.query(condition)


# ============================================================
# Count students
# ============================================================

def count_students(df):
    """
    Count the number of students.
    """

    return len(df)


# ============================================================
# Find student with highest GPA
# ============================================================

def highest_gpa(df):
    """
    Find the student with the highest GPA.
    """

    max_gpa = df["GPA"].max()
    student = df[df["GPA"] == max_gpa]

    return student


# ============================================================
# Process user question
# ============================================================

def analyze_student_data(file, question):
    """
    Analyze the uploaded student CSV file according to
    the user's natural language question.
    """

    try:

        # Check that a file was uploaded
        if file is None:
            return "Please upload a CSV file."

        # Load CSV
        df = pd.read_csv(file.name)

        # Convert question to lowercase
        q = question.lower().strip()

        # ----------------------------------------------------
        # Average GPA
        # ----------------------------------------------------

        if "average" in q and "gpa" in q:

            average = df["GPA"].mean()

            return f"Average GPA = {average:.2f}"


        # ----------------------------------------------------
        # Highest GPA
        # ----------------------------------------------------

        elif "highest" in q and "gpa" in q:

            student = highest_gpa(df)

            result = student.to_string(index=False)

            return f"Student with the highest GPA:\n\n{result}"


        # ----------------------------------------------------
        # Number of students
        # ----------------------------------------------------

        elif (
            "number of students" in q
            or "how many students" in q
            or "count students" in q
        ):

            count = count_students(df)

            return f"Number of students = {count}"


        # ----------------------------------------------------
        # Students with GPA greater than 3.5
        # ----------------------------------------------------
        elif (
            "gpa > 3.5" in q
            or "gpa greater than 3.5" in q
            or "above 3.5" in q
            or "more than 3.5" in q
        ):

            result = df[df["GPA"] > 3.5]

            if result.empty:
                return "No students have GPA greater than 3.5."

            return result.to_string(index=False)


        # ----------------------------------------------------
        # Show all students
        # ----------------------------------------------------

        elif (
            "show all" in q
            or "all students" in q
            or "display students" in q
        ):

            return df.to_string(index=False)


        # ----------------------------------------------------
        # Unknown question
        # ----------------------------------------------------

        else:

            return (
                "I could not understand the question.\n\n"
                "Try one of these examples:\n"
                "- What is the average GPA?\n"
                "- Who has the highest GPA?\n"
                "- How many students are there?\n"
                "- Show students with GPA greater than 3.5"
            )


    except Exception as e:

        return f"Error: {str(e)}"


# ============================================================
# Gradio Interface
# ============================================================

with gr.Blocks(title="Smart Student Data Analysis Agent") as demo:

    gr.Markdown(
        """
        # 🎓 Smart Student Data Analysis Agent

        Upload a student CSV file and ask questions about the data
        using natural language.
        """
    )

    # CSV upload
    file_input = gr.File(
        label="Upload Student CSV File",
        file_types=[".csv"]
    )

    # User question
    question_input = gr.Textbox(
        label="Ask a Question",
        placeholder="Example: What is the average GPA?"
    )

    # Analyze button
    analyze_button = gr.Button("Analyze")

    # Result
    result_output = gr.Textbox(
        label="Result",
        lines=10
    )

    # Connect button to function
    analyze_button.click(
        fn=analyze_student_data,
        inputs=[file_input, question_input],
        outputs=result_output
    )


# ============================================================
# Run the application
# ============================================================

if __name__ == "__main__":

    demo.launch()