# Smart Student Data Analysis Agent Using Smolagents

## Project Overview

**Smart Student Data Analysis Agent** is an AI-powered student data analysis system developed using **Smolagents**, **Python**, **Pandas**, **LiteLLM**, **Ollama**, and **Qwen2.5:1.5B**.

The system allows users to upload a student CSV dataset and ask questions in natural language. The AI agent analyzes the data using Python tools and returns the requested result.

## System Architecture

```text
User
  ↓
Gradio User Interface
  ↓
Smolagents CodeAgent
  ↓
LiteLLM
  ↓
Ollama
  ↓
Qwen2.5:1.5B
  ↓
Python / Pandas Tools
  ↓
Student CSV Dataset
  ↓
Analysis Result
```

## Main Features

- Upload a student CSV file through the graphical interface.
- Ask questions using natural language.
- Calculate the average GPA.
- Find the student with the highest GPA.
- Count the total number of students.
- Count students above a specified GPA threshold.
- Validate GPA threshold values.
- Analyze the uploaded dataset using Python and Pandas.
- Use a local LLM through Ollama.
- Use Smolagents for tool-based agent execution.

## User Interface

The project uses **Gradio** to provide a simple graphical interface.

The user can:

1. Upload a CSV file.
2. Enter a natural-language question.
3. Submit the question.
4. Receive the analysis result from the agent.

## Example Results

The system was tested successfully using a dataset containing 10 students.

Example queries and results:

- **Average GPA:** 3.39
- **Highest GPA:** Huda, GPA 3.9
- **Number of students:** 10
- **Students with GPA above 3.5:** 4
- **Students above the average GPA:** 6

The system also validates invalid GPA thresholds. For example, a threshold greater than 4 is rejected.

## Technologies Used

- Python
- Pandas
- Smolagents
- Gradio
- LiteLLM
- Ollama
- Qwen2.5:1.5B
- Git
- GitHub

## Project Structure

```text
project/
│
├── agent.py
├── app.py
├── tools.py
├── requirements.txt
│
└── data/
    └── students.csv
```

## File Description

### `agent.py`

Contains the Smolagents **CodeAgent**, the local LLM configuration, and the data-analysis tools used by the agent.

### `app.py`

Contains the **Gradio User Interface** for uploading CSV files and asking questions.

### `tools.py`

Contains the Python functions used for loading and analyzing student data.

### `data/students.csv`

Contains the sample student dataset used for testing.

### `requirements.txt`

Contains the Python dependencies required to run the project.

## How the System Works

The user first uploads a CSV dataset through the Gradio interface.

The natural-language question is then passed to the Smolagents agent.

The agent selects the appropriate Python tool, which uses Pandas to analyze the student dataset.

The result is returned to the user through the Gradio interface.

## Local LLM

The project uses a locally running language model through **Ollama**.

The current model is:

```text
Qwen2.5:1.5B
```

The architecture avoids sending the student dataset to an external LLM service for the analysis tools.

## Testing

The project was tested with several student-data questions, including:

```text
What is the average GPA?
Who has the highest GPA?
How many students are there?
How many students have GPA above 3.5?
How many students are above the average GPA?
```

All five main test cases produced the expected results.

## Future Development

Possible future improvements include:

- Adding more data-analysis tools.
- Supporting additional student-data questions.
- Improving natural-language understanding.
- Adding more validation and error handling.
- Adding agent memory and state management.
- Improving security and execution restrictions.
- Adding data visualization.
- Expanding the evaluation and testing framework.

## Project Status

**Current Status: Working Prototype**

The project currently includes a working Gradio interface, Smolagents CodeAgent, local Ollama/Qwen LLM integration, Python/Pandas analysis tools, CSV upload, and tested student-data analysis functions.