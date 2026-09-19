Smart Student Data Analysis Agent Using Smolagents

Project Overview

This project is a Smart Student Data Analysis Agent developed using Smolagents.

The main goal of the project is to allow an AI agent to analyze student data and answer questions based on a CSV dataset.

The project is being developed incrementally, and this submission represents the initial working prototype.

Current Progress

The following components have been implemented and tested successfully:

1. Student Dataset

A sample student dataset is stored in:

data/students.csv

The dataset contains information such as:

- Student ID
- Name
- Age
- Gender
- Department
- GPA

2. Data Loading Tool

The "load_data()" function in "tools.py" loads the student dataset using Pandas.

3. Statistical Analysis

The "calculate_statistics()" function calculates basic GPA statistics, including:

- Number of students
- Average GPA
- Maximum GPA
- Minimum GPA

4. Student Filtering

The "filter_students()" function allows students to be filtered according to a specific condition, such as:

GPA > 3.5

5. Smolagents Integration

The project uses Smolagents CodeAgent to create an AI agent capable of selecting and using tools.

6. LLM Integration

The current model architecture is:

Smolagents
     ↓
LiteLLM
     ↓
Ollama
     ↓
Qwen2.5:1.5B

The model is running locally through Ollama.

7. Tool-Based Data Analysis

The agent was tested with the question:

What is the average GPA of the students?

Instead of manually providing or inventing student values, the agent uses a Python tool to calculate the average GPA directly from:

data/students.csv

The current dataset contains 10 students, and the calculated average GPA is:

3.39

Current System Architecture

User Question
      ↓
Smolagents Agent
      ↓
Tool Selection
      ↓
Python / Pandas
      ↓
Student CSV Dataset
      ↓
Analysis Result
      ↓
Agent Answer

Technologies Used

- Python
- Pandas
- Smolagents
- LiteLLM
- Ollama
- Qwen2.5:1.5B
- GitHub

Project Structure

MathDataAgent/
│
├── agent.py
├── tools.py
├── requirements.txt
├── README.md
│
└── data/
    └── students.csv

Future Development

The next stages of the project will include:

- Adding more data analysis tools.
- Supporting more natural-language questions.
- Adding validation and error handling.
- Implementing Agent planning and multi-step reasoning.
- Adding memory/state management.
- Adding security and execution restrictions.
- Developing a graphical user interface for CSV upload and analysis.
- Evaluating the agent using different test cases.

Status

Current Status: Initial Working Prototype

The data loading, analysis tools, Smolagents integration, and local LLM connection have been implemented and tested successfully.
