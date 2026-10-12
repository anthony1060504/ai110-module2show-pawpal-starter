from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Pet care setup")
owner_name = st.text_input("Owner name", value="Jordan")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
    species = st.selectbox("Species", ["dog", "cat", "other"], key="species")
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    pet_name = pet_name.strip()
    if pet_name:
        pet = Pet(name=pet_name, species=species)
        st.session_state.owner.add_pet(pet)
        st.session_state.active_pet_index = len(st.session_state.owner.pets) - 1
        st.session_state.schedule = None
        st.success(f"Added {pet.name}.")
    else:
        st.error("Enter a pet name before adding a pet.")

owner = st.session_state.owner
active_pet = None
if owner.pets:
    active_pet_index = st.selectbox(
        "Active pet",
        options=range(len(owner.pets)),
        format_func=lambda index: f"{owner.pets[index].name} ({owner.pets[index].species})",
        key="active_pet_index",
    )
    active_pet = owner.pets[active_pet_index]
    st.table([{"Name": pet.name, "Species": pet.species} for pet in owner.pets])
else:
    st.info("Add a pet to start planning care.")

if active_pet is not None:
    st.subheader(f"Tasks for {active_pet.name}")
    with st.form("add_task_form"):
        task_title = st.text_input("Task title", value="Morning walk", key="task_title")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration"
        )
        priority = st.selectbox(
            "Priority", ["low", "medium", "high"], index=2, key="task_priority"
        )
        add_task = st.form_submit_button("Add task")

    if add_task:
        task_title = task_title.strip()
        if task_title:
            active_pet.add_task(
                Task(
                    title=task_title,
                    duration_minutes=int(duration),
                    priority=priority,
                )
            )
            st.session_state.schedule = None
            st.success("Task added.")
        else:
            st.error("Enter a task title before adding a task.")

    if active_pet.tasks:
        st.table(
            [
                {
                    "Task": task.title,
                    "Duration (minutes)": task.duration_minutes,
                    "Priority": task.priority,
                }
                for task in active_pet.tasks
            ]
        )
    else:
        st.info("No tasks for this pet yet.")

    st.subheader("Build schedule")
    start_time = st.time_input("Start time", value=time(8, 0), key="schedule_start_time")
    time_budget = st.number_input(
        "Time budget (minutes)",
        min_value=1,
        max_value=1440,
        value=120,
        step=15,
        key="schedule_time_budget",
    )

    schedule_signature = (active_pet_index, start_time, int(time_budget))
    if st.button("Generate schedule", disabled=not active_pet.tasks, key="generate_schedule"):
        scheduler = Scheduler()
        scheduled_tasks = scheduler.create_daily_schedule(
            owner=owner,
            pet=active_pet,
            start_time=start_time,
            time_budget_minutes=int(time_budget),
        )
        st.session_state.schedule = {
            "signature": schedule_signature,
            "tasks": scheduler.sort_by_time(scheduled_tasks),
            "conflicts": scheduler.detect_conflicts([active_pet]),
        }

    schedule = st.session_state.get("schedule")
    if schedule is not None and schedule["signature"] == schedule_signature:
        st.write("Daily schedule")
        st.table(
            [
                {
                    "Task": task.title,
                    "Status": "Scheduled" if task.scheduled else "Not scheduled",
                    "Start": task.start_time.strftime("%H:%M") if task.start_time else "",
                    "End": task.end_time.strftime("%H:%M") if task.end_time else "",
                    "Reason": task.reason,
                }
                for task in schedule["tasks"]
            ]
        )
        if schedule["conflicts"]:
            for conflict in schedule["conflicts"]:
                st.warning(
                    f"{conflict} Please review these times and adjust one task if needed."
                )
        else:
            st.success("No overlapping tasks found in this schedule.")
    elif active_pet.tasks:
        st.info("Generate a schedule to see planned task times.")
