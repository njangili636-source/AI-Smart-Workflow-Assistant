import streamlit as st
import database
import requests
from datetime import date, datetime

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="AI Smart Workflow Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = ""

if "schedule_result" not in st.session_state:
    st.session_state.schedule_result = ""


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #eef2ff, #fdf2f8, #eff6ff);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #312e81, #6d28d9, #9333ea);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.title {
    font-size: 38px;
    font-weight: bold;
    color: #4c1d95;
}

.subtitle {
    color: #64748b;
    font-size: 17px;
}

h1, h2, h3 {
    color: #312e81;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff, #ede9fe);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #c4b5fd;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.12);
}

.stButton button {
    background: linear-gradient(90deg, #7c3aed, #2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    height: 45px;
}

.stButton button:hover {
    background: linear-gradient(90deg, #db2777, #7c3aed);
    color: white;
    border: none;
}

div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input {
    border-radius: 10px;
    border: 1px solid #a78bfa;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.title("🤖 AI Workflow")

st.sidebar.write("Your Personal AI Assistant")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📝 Task Manager",
        "🤖 AI Workflow Generator",
        "📅 Smart Scheduling",
        "📊 Workflow History",
        "📈 Schedule Progress Tracker"
    ]
)

st.sidebar.divider()

st.sidebar.success("AI Assistant Ready")

st.sidebar.caption("Powered by Python + Ollama")


# ---------------- DASHBOARD ----------------

if page == "🏠 Dashboard":

    st.markdown(
        '<p class="title">AI Smart Workflow Assistant</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Manage your tasks intelligently using AI automation.</p>',
        unsafe_allow_html=True
    )

    st.divider()

    tasks = database.get_tasks()
    workflows = database.get_workflows()

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks if task[3] == 1
    )

    pending_tasks = total_tasks - completed_tasks

    total_workflows = len(workflows)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📝 Total Tasks", total_tasks)

    with col2:
        st.metric("✅ Completed Tasks", completed_tasks)

    with col3:
        st.metric("🤖 AI Workflows", total_workflows)

    st.subheader("📊 Overall Task Progress")

    if total_tasks > 0:

        progress = completed_tasks / total_tasks

        st.progress(progress)

        st.success(
            f"Completion Progress: {progress * 100:.1f}%"
        )

    else:

        st.info("Add tasks to start tracking progress.")

    st.divider()

    st.subheader("Welcome to Your Dashboard 👋")

    st.write(
        "This application uses Artificial Intelligence "
        "to convert your tasks into organized workflows."
    )

    st.info(
        "Select AI Workflow Generator from the sidebar "
        "to create your first workflow."
    )

    st.subheader("Application Features")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("""
        **📝 Task Management**

        Organize your daily activities and assignments.

        **🤖 AI Automation**

        Automatically generate task workflows.

        **📈 Schedule Progress Tracker**

        Track completed and pending activities.
        """)

    with c2:

        st.markdown("""
        **📅 Smart Scheduling**

        Get suggested schedules for your tasks.

        **📊 Workflow History**

        View previously generated workflows.
        """)


# ---------------- TASK MANAGER ----------------

elif page == "📝 Task Manager":

    st.title("📝 Task Manager")

    st.write(
        "Manage your tasks with permanent database storage."
    )

    st.subheader("➕ Add New Task")

    task_name = st.text_input("Enter Task Name")

    priority = st.selectbox(
        "Select Priority",
        ["High", "Medium", "Low"]
    )

    if st.button("Add Task"):

        if task_name.strip():

            database.add_task(task_name, priority)

            st.success("Task saved successfully!")

            st.rerun()

        else:

            st.warning("Please enter a task name.")

    st.divider()

    st.subheader("📋 Your Saved Tasks")

    tasks = database.get_tasks()

    if tasks:

        for task in tasks:

            task_id, name, priority, completed = task

            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:

                new_status = st.checkbox(
                    name,
                    value=bool(completed),
                    key=f"task_{task_id}"
                )

                if new_status != bool(completed):

                    database.update_task(
                        task_id,
                        new_status
                    )

                    st.rerun()

            with col2:

                if priority == "High":

                    st.error("🔴 High")

                elif priority == "Medium":

                    st.warning("🟡 Medium")

                else:

                    st.success("🟢 Low")

            with col3:

                if st.button(
                    "🗑️",
                    key=f"delete_{task_id}"
                ):

                    database.delete_task(task_id)

                    st.rerun()

        st.divider()

        total = len(tasks)

        completed_count = sum(
            1 for task in tasks if task[3] == 1
        )

        pending = total - completed_count

        st.subheader("📊 Task Progress")

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Tasks", total)

        c2.metric("Completed", completed_count)

        c3.metric("Pending", pending)

        progress = completed_count / total

        st.progress(progress)

        st.success(
            f"Your progress: {progress * 100:.1f}%"
        )

    else:

        st.info("No tasks available. Add your first task!")


# ---------------- AI WORKFLOW GENERATOR ----------------

elif page == "🤖 AI Workflow Generator":

    st.title("🤖 AI Workflow Generator")

    st.write(
        "Enter your task and let AI automatically "
        "create an organized workflow."
    )

    task = st.text_area(
        "Describe Your Task",
        placeholder="Example: Complete DSA assignment and prepare for exams."
    )

    deadline = st.text_input(
        "Enter Your Deadline",
        placeholder="Example: 25 November 2026"
    )

    if st.button("Generate AI Workflow 🚀"):

        if task.strip():

            prompt = f"""
You are an intelligent AI workflow automation assistant.

TASK:
{task}

DEADLINE:
{deadline if deadline.strip() else "Not specified"}

Create a detailed and practical workflow.

Include:

1. TASK ANALYSIS
2. TASK BREAKDOWN
3. STEP-BY-STEP INSTRUCTIONS
4. TIME ESTIMATION
5. PRIORITY LEVEL
6. DAILY ACTION PLAN
7. REQUIRED RESOURCES
8. PROGRESS CHECKLIST
9. FINAL RECOMMENDATIONS

IMPORTANT:
- Do not give only general suggestions.
- Explain exactly what actions the user should perform.
- Use simple English.
- Make the workflow realistic and achievable.
"""

            with st.spinner("AI is generating your workflow..."):

                try:

                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": "qwen2.5-coder:7b",
                            "prompt": prompt,
                            "stream": False,
                            "options": {
                                "num_predict": 700,
                                "temperature": 0.3
                            }
                        },
                        timeout=600
                    )

                    response.raise_for_status()

                    result = response.json()["response"]

                    st.session_state.result = result

                    database.save_workflow(task, result)

                    st.session_state.history.append({
                        "task": task,
                        "deadline": deadline,
                        "result": result,
                        "date": datetime.now().strftime(
                            "%d-%m-%Y %H:%M"
                        )
                    })

                    st.success(
                        "Workflow Generated and Saved Successfully!"
                    )

                except requests.exceptions.RequestException as e:

                    st.error(f"Ollama connection error: {e}")

                except (KeyError, ValueError) as e:

                    st.error(f"Invalid AI response: {e}")

        else:

            st.warning("Please enter your task.")

    if st.session_state.result:

        st.divider()

        st.subheader("Your AI-Generated Workflow")

        st.markdown(st.session_state.result)

        st.download_button(
            label="📥 Download Workflow Report",
            data=st.session_state.result,
            file_name="AI_Workflow_Report.txt",
            mime="text/plain"
        )


# ---------------- SMART SCHEDULING ----------------

elif page == "📅 Smart Scheduling":

    st.title("📅 Smart Scheduling")

    st.write(
        "Create a personalized daily schedule using AI."
    )

    st.divider()

    st.subheader("📋 Schedule Details")

    schedule_task = st.text_input(
        "Enter Your Task",
        placeholder="Example: Complete DSA Assignment"
    )

    today = date.today()

    deadline = st.date_input(
        "Select Deadline",
        value=today
    )

    available_hours = st.number_input(
        "Available Study Hours Per Day",
        min_value=1,
        max_value=12,
        value=3
    )

    if st.button("📅 Generate Smart Schedule"):

        if not schedule_task.strip():

            st.warning("Please enter your task.")

        elif deadline < today:

            st.error("Please select today or a future deadline.")

        else:

            days_remaining = (deadline - today).days + 1

            prompt = f"""
You are an intelligent AI scheduling assistant.

Today's Date: {today}

Task: {schedule_task}

Deadline: {deadline}

Days Available: {days_remaining}

Available Study Hours Per Day: {available_hours}

Create a realistic daily schedule starting from TODAY.

IMPORTANT RULES:

1. Start the schedule from {today}.
2. Never use dates before today.
3. Finish all activities on or before the deadline.
4. Use the correct dates.
5. Divide the work into daily activities.
6. Include estimated time for each activity.
7. Include High, Medium and Low priority levels.
8. Include suitable break times.
9. Do not exceed {available_hours} study hours per day.
10. Use simple English.

GENERATE:

1. Task Overview
2. Days Available
3. Daily Schedule
4. Activities for Each Day
5. Estimated Time
6. Priority Levels
7. Break Times
8. Final Deadline Checklist

Explain exactly what the user should do each day.
"""

            with st.spinner("AI is preparing your schedule..."):

                try:

                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": "qwen2.5-coder:7b",
                            "prompt": prompt,
                            "stream": False,
                            "options": {
                                "num_predict": 700,
                                "temperature": 0.3
                            }
                        },
                        timeout=600
                    )

                    response.raise_for_status()

                    schedule_result = response.json()["response"]

                    st.session_state.schedule_result = schedule_result

                    database.save_workflow(
                        "Smart Schedule: " + schedule_task,
                        schedule_result
                    )

                    st.success(
                        "Your Smart Schedule was generated and saved!"
                    )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Ollama connection error: {e}"
                    )

                except (KeyError, ValueError) as e:

                    st.error(
                        f"Invalid AI response: {e}"
                    )

    if st.session_state.schedule_result:

        st.divider()

        st.subheader(
            "📅 Your Personalized Daily Schedule"
        )

        st.markdown(
            st.session_state.schedule_result
        )

        st.download_button(
            label="📥 Download Schedule",
            data=st.session_state.schedule_result,
            file_name="Smart_Schedule.txt",
            mime="text/plain"
        )

    else:

        st.info(
            "Enter your task details above to generate a smart schedule."
        )


# ---------------- WORKFLOW HISTORY ----------------

elif page == "📊 Workflow History":

    st.title("📊 Workflow History")

    st.write(
        "Your previously generated workflows."
    )

    workflows = database.get_workflows()

    if workflows:

        for item in workflows:

            workflow_id, task, result, created_at = item

            with st.expander(
                f"Workflow {workflow_id}: {task[:50]}"
            ):

                st.write("Task:", task)

                st.write("Generated:", created_at)

                st.markdown(result)

                st.download_button(
                    label="📥 Download Workflow",
                    data=result,
                    file_name=f"Workflow_{workflow_id}.txt",
                    mime="text/plain",
                    key=f"download_{workflow_id}"
                )

    else:

        st.info(
            "No workflow history available yet."
        )


# ---------------- SCHEDULE PROGRESS TRACKER ----------------

elif page == "📈 Schedule Progress Tracker":

    st.title("📈 Schedule Progress Tracker")

    st.write(
        "Track your daily activities and monitor your completion progress."
    )

    st.divider()

    # Add Activity

    st.subheader("➕ Add Daily Activity")

    schedule_name = st.text_input(
        "Schedule Name",
        placeholder="Example: DSA Preparation"
    )

    activity = st.text_input(
        "Enter Activity",
        placeholder="Example: Study Dijkstra Algorithm"
    )

    if st.button("Add Activity"):

        if schedule_name.strip() and activity.strip():

            database.add_schedule_activity(
                schedule_name,
                activity
            )

            st.success("Activity added successfully!")

            st.rerun()

        else:

            st.warning(
                "Please enter both schedule name and activity."
            )

    st.divider()

    # Get Activities

    activities = database.get_schedule_activities()

    st.subheader("📋 Your Daily Activities")

    if activities:

        total = len(activities)

        completed = sum(
            1 for item in activities if item[3] == 1
        )

        pending = total - completed

        progress = completed / total

        # Metrics

        col1, col2, col3 = st.columns(3)

        col1.metric("📋 Total Activities", total)

        col2.metric("✅ Completed", completed)

        col3.metric("⏳ Pending", pending)

        # Progress Bar

        st.subheader("📊 Overall Progress")

        st.progress(progress)

        st.success(
            f"You have completed {progress * 100:.1f}% of your activities!"
        )

        st.divider()

        # Activity List

        st.subheader("📝 Manage Activities")

        for item in activities:

            activity_id, schedule, activity_name, status, created_at = item

            st.markdown(f"**📅 {schedule}**")

            col1, col2 = st.columns([5, 1])

            with col1:

                new_status = st.checkbox(
                    activity_name,
                    value=bool(status),
                    key=f"schedule_activity_{activity_id}"
                )

                if new_status != bool(status):

                    database.update_schedule_activity(
                        activity_id,
                        new_status
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_activity_{activity_id}"
                ):

                    database.delete_schedule_activity(
                        activity_id
                    )

                    st.rerun()

            st.divider()

        # Pending Activities

        st.subheader("⏳ Pending Activities")

        pending_activities = [
            item for item in activities if item[3] == 0
        ]

        if pending_activities:

            for item in pending_activities:

                st.warning(
                    f"• {item[2]} — {item[1]}"
                )

        else:

            st.success(
                "🎉 Congratulations! All activities are completed!"
            )

    else:

        st.info(
            "No activities available. Add your first daily activity!"
        )


# ---------------- FOOTER ----------------

st.sidebar.divider()

st.sidebar.caption(
    "AI Smart Workflow Assistant | 2026"
)