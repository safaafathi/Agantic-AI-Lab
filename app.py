# ============================================================
# Smart Student Data Analysis Agent
# Gradio + Smolagents + Ollama + Qwen
# ============================================================

import gradio as gr
import tools

from agent import run_with_memory


# ============================================================
# 1. Analyze Student Data
# ============================================================

def analyze_student_data(file, question):

    if file is None:
        return "Please upload a CSV file first."

    if not question or not question.strip():
        return "Please enter a question."

    try:
        # Get uploaded CSV file path
        file_path = file.name

        # Set the uploaded file as the current data file
        tools.set_data_file(file_path)

        # Send question to the Agent
        result = run_with_memory(question)

        return str(result)

    except Exception as e:

        return f"Error: {str(e)}"


# ============================================================
# 2. Gradio Interface
# ============================================================

with gr.Blocks(
    title="Smart Student Data Analysis Agent"
) as demo:

    gr.Markdown(
        """
        # 🎓 Smart Student Data Analysis Agent

        ### Analyze student data using Artificial Intelligence

        Upload a student CSV file and ask questions about the data
        using natural language.

        Technologies:
        Gradio • Smolagents • Ollama • Qwen • Python • Pandas
        """
    )


    # ========================================================
    # File Upload
    # ========================================================

    file_input = gr.File(
        label="📂 Upload Student CSV File",
        file_types=[".csv"]
    )


    # ========================================================
    # Question Input
    # ========================================================

    question_input = gr.Textbox(
        label="💬 Ask a Question",
        placeholder="Example: What is the average GPA?",
        lines=2
    )


    # ========================================================
    # Example Questions
    # ========================================================

    gr.Markdown("### 💡 Example Questions")

    gr.Examples(
        examples=[
            ["What is the average GPA?"],
            ["Who is the student with the highest GPA?"],
            ["What is the best GPA in the dataset?"],
            ["How many students have GPA above 3.5?"],
            ["How many students are above the average?"],
            ["How many students are there?"]
        ],
        inputs=question_input
    )


    # ========================================================
    # Analyze Button
    # ========================================================

    analyze_button = gr.Button(
        "🔍 Analyze",
        variant="primary"
    )


    # ========================================================
    # Result
    # ========================================================

    result_output = gr.Textbox(
        label="📊 Analysis Result",
        lines=6
    )


    # ========================================================
    # Button Action
    # ========================================================

    analyze_button.click(
        fn=analyze_student_data,
        inputs=[
            file_input,
            question_input
        ],
        outputs=result_output
    )


# ============================================================
# 3. Run Application
# ============================================================

if __name__ == "__main__":

    demo.launch()