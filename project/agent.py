from smolagents import CodeAgent, LiteLLMModel, tool
from tools import load_data


# ==========================================
# 1. Connect to Ollama
# ==========================================

model = LiteLLMModel(
    model_id="ollama/qwen2.5:1.5b",
    api_base="http://localhost:11434"
)


# ==========================================
# 2. Tool: Calculate Average GPA
# ==========================================

@tool
def calculate_average_gpa() -> float:
    """
    Calculate the average GPA from the student CSV dataset.

    Returns:
        The exact average GPA calculated from data/students.csv.
    """
    df = load_data()
    return float(df["GPA"].mean())


# ==========================================
# 3. Create Agent
# ==========================================

agent = CodeAgent(
    tools=[
        calculate_average_gpa
    ],
    model=model,
    max_steps=3
)


# ==========================================
# 4. Ask the Agent
# ==========================================

question = "What is the average GPA of the students?"

print("\nQuestion:")
print(question)

print("\nAgent Answer:")

answer = agent.run(
    question,
    additional_args={
        "instructions": """
        You must use the calculate_average_gpa tool to answer this question.
        Do not invent student data.
        Do not calculate the GPA from numbers provided by yourself.
        The answer must come from the student CSV dataset through the tool.
        """
    }
)

print(answer)