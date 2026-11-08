# Smart Student Data Analysis Agent Using Smolagents 🎓🤖

A student-data analysis prototype in the education domain. It lets a user upload a CSV file and ask questions about student records in natural language. The application validates the uploaded data, uses Python and Pandas for supported statistical calculations, and provides a Gradio interface. A Smolagents `CodeAgent` is configured with a locally hosted `Qwen2.5:1.5B` model through Ollama and LiteLLM for agent-based handling.

> **Project status:** Educational prototype, not a production student-information system. The current application provides read-only analysis. It does not modify student records or implement an in-app approval gate. Important results must be checked by a human before being used.

---

## 1. What It Does

The agent analyzes student CSV data, including fields such as `Student_ID`, `Name`, `Age`, `Gender`, `Department`, and `GPA`. It supports tasks such as:

- Calculating the average GPA across the dataset.
- Identifying the student with the highest GPA.
- Counting students above a specific GPA threshold.
- Counting students above the dataset average GPA.
- Validating GPA thresholds against the supported range of $0 \le \text{GPA} \le 4$.

---

## 2. Prerequisites

- **Python:** 3.12
- **Git:** To clone the repository.
- **Ollama:** Installed and running locally.
- **Model:** `qwen2.5:1.5b` downloaded in Ollama.
- **Operating System:** Windows instructions are shown below (commands can be easily adapted for macOS/Linux).

The tested project stack includes **Python**, **Pandas**, **Smolagents**, **LiteLLM**, **Ollama**, **Qwen2.5:1.5B**, and **Gradio**.

---

## 3. Installation

Open PowerShell or your terminal and run:

```bash
# 1. Clone the repository
git clone https://github.com/safaafathi/Agantic-AI-Lab.git
cd Agantic-AI-Lab

# 2. Create and activate a virtual environment
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# If PowerShell blocks activation, use Command Prompt:
# .venv\Scripts\activate.bat

# 3. Install project dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Download and run the Ollama model
ollama pull qwen2.5:1.5b
```

> **Note:** Ollama must be running locally before using the model. The first model download requires an internet connection and approximately 1 GB of disk space; subsequent local inference does not require a hosted model API.

---

## 4. Configuration

### Current Configuration

The tested project configuration uses the local Ollama model:
- **Model ID:** `ollama/qwen2.5:1.5b`
- **Ollama API Endpoint:** `http://localhost:11434`

In the current implementation, these settings are configured directly in the Python source code. The project does not currently read model-provider settings from a `.env` file, nor does it provide environment variables for switching between local and hosted model providers.

> 🔒 **Security Notice:** Do not create or commit a real `.env` file containing secrets. If provider switching is added in a later version, document the exact variable names in `.env.example` and keep `.env` excluded via `.gitignore`.

---

## 5. Running the Application

Make sure your virtual environment is active and Ollama is running, then execute from the repository root:

```bash
python app.py
```

When startup succeeds, the terminal will display a local Gradio URL (typically `http://127.0.0.1:7860`). Open the address in your browser, upload a student CSV file, and begin asking questions in natural language.

---

## 6. Testing & Evaluation

The project includes a 7-case evaluation routine in `agent.py`, covering principal calculations and handling of invalid GPA thresholds.

Run the evaluation from the repository root:

```powershell
.\.venv\Scripts\python.exe agent.py
```

The evaluation was verified locally and achieved a **7/7 (100%) pass rate** on the selected test set. Verified checks include:
1. Average GPA calculation.
2. Highest-GPA student identification.
3. Number of students above a GPA threshold (3.5).
4. Number of students above the dataset average.
5. Total number of student records.
6. Rejection of an out-of-range GPA threshold.
7. Rejection of another invalid threshold value.

---

## 7. Worked Example

Using the included 10-record sample dataset, the following questions produce these reference results:

| Question | Expected Result |
| :--- | :--- |
| **How many students are in the dataset?** | `10` |
| **What is the average GPA?** | `3.39` |
| **Who has the highest GPA?** | `Huda (3.90)` |
| **How many students have a GPA above 3.5?** | `4` |
| **How many students are above the average GPA?** | `6` |
| **Count students above GPA threshold 5** | `Validation error: threshold must be between 0 and 4` |

---

## 8. Reproducing the Evaluation

To execute the test suite independently:

```powershell
.\.venv\Scripts\python.exe agent.py
```

*Note: The verified local evaluation achieved 7/7 passing cases using the 10-student sample dataset. This result is limited to the selected evaluation cases and does not represent a general accuracy guarantee.*

---

## 9. Approval Gate & Human Oversight

The current prototype has **no in-app approval gate**. It performs read-only analysis and contains no tools for modifying student records or triggering consequential institutional decisions.

- **Human Oversight:** Human review is procedural — an authorized person must independently verify analytical results against the source data before taking action.
- **Future Considerations:** If consequential actions are introduced in future releases, they must remain disabled until explicit authorization workflows, role-based access checks, and an audit log are implemented and thoroughly tested.

---

## 10. Repository Map

```text
├── agent.py          # Agent setup, model connection, analysis & evaluation logic
├── app.py            # Gradio web application user interface
├── tools.py          # Data-loading, validation, and analysis tools
├── requirements.txt  # Python package dependencies
├── data/             # Sample student CSV datasets
├── week 1/ - week 4/ # Coursework & lab modules associated with the project
└── project/          # Additional project-related materials
```

---

## 11. Limitations & Evaluation Summary

### Limitations

- **Dataset Size:** Evaluation dataset currently contains only 10 student records.
- **Schema Dependent:** The implementation expects specific CSV column headers (e.g., `Name`, `GPA`).
- **Benchmark:** Formal latency and execution cost benchmarks have not been performed.
- **Authentication:** Lacks institutional authentication, role-based access control (RBAC), and persistent conversation memory.
- **Data Privacy:** Synthetic or anonymized data should be used for public demonstrations. Never commit real student records or credentials.

### Evaluation Summary Table

| Measure | Recorded Result |
| :--- | :--- |
| **Dataset Size** | 10 students |
| **Average GPA** | 3.39 |
| **Highest GPA** | Huda ($3.90$) |
| **Students above 3.5 GPA** | 4 |
| **Students above Average GPA** | 6 |
| **Selected Evaluation Cases Passed** | **7 / 7** |

---

## Acknowledggements

This project utilizes open-source software and tools, including:
- [Hugging Face Smolagents](https://github.com/huggingface/smolagents)
- [Pandas](https://pandas.pydata.org/)
- [Gradio](https://www.gradio.app/)
- [LiteLLM](https://github.com/BerriAI/litellm)
- [Ollama](https://ollama.com/) & [Qwen2.5](https://huggingface.org/Qwen/Qwen2.5-1.5B)