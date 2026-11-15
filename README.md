# 🤖 AI Smart Workflow Assistant

## 📌 Project Description

AI Smart Workflow Assistant is an AI-powered application developed using Python and Streamlit. It helps users organize daily tasks, generate intelligent workflows, create schedules, and track task completion.

The application uses a locally running AI model through Ollama to generate personalized workflows and schedules.

## ✨ Features

1. **Dashboard** – View project activities and task summaries.
2. **Task Manager** – Add, update, and delete tasks.
3. **AI Workflow Generator** – Generate workflows using AI.
4. **Smart Scheduling** – Create AI-powered schedules.
5. **Workflow History** – View previously generated workflows.
6. **Schedule Progress Tracker** – Monitor completed and pending activities.

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite Database
- Ollama
- Qwen 2.5 Coder 7B
- Requests

## 📂 Project Structure

```text
AI-Smart-Workflow-Assistant/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── workflow
├── venv/
└── __pycache__/
```

Note: The virtual environment, cache, and local database should not be uploaded to GitHub.

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### Step 2: Open the Project Folder

```bash
cd AI-Smart-Workflow-Assistant
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Ollama Model

Install Ollama and download the model:

```bash
ollama pull qwen2.5-coder:7b
```

### Step 5: Run the Application

Start Ollama and execute:

```bash
streamlit run app.py
```

## 🗄️ Database

SQLite is used to store:
- User tasks
- Generated workflows
- Schedule activities
- Completion status

The database tables are automatically created by `database.py`.

## 🎯 Project Objective

The main objective is to simplify task management and improve productivity through AI-powered workflow generation, smart scheduling, and progress tracking.

## 👨‍💻 Developed As

Academic Student Project

## 📌 Future Enhancements

- User authentication
- Cloud database integration
- Email notifications
- Advanced AI recommendations
- Deployment with Streamlit Community Cloud