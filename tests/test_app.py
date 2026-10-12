from datetime import time
from pathlib import Path

from streamlit.testing.v1 import AppTest

from pawpal_system import Owner, Pet, Scheduler, Task


def test_pet_task_schedule_flow() -> None:
	app_path = Path(__file__).resolve().parents[1] / "app.py"
	app_test = AppTest.from_file(str(app_path)).run()
	assert not app_test.exception

	app_test.text_input(key="pet_name").set_value("Mochi")
	next(button for button in app_test.button if button.label == "Add pet").click().run()
	assert not app_test.exception
	owner = app_test.session_state["owner"]
	assert len(owner.pets) == 1
	assert owner.pets[0].name == "Mochi"
	assert "Mochi" in str(app_test.table[0].value)

	app_test.text_input(key="task_title").set_value("Morning walk")
	app_test.number_input(key="task_duration").set_value(20)
	next(button for button in app_test.button if button.label == "Add task").click().run()
	assert not app_test.exception
	assert len(owner.pets[0].tasks) == 1
	task = owner.pets[0].tasks[0]
	assert task.title == "Morning walk"

	app_test.button(key="generate_schedule").click().run()
	assert not app_test.exception
	assert task.scheduled
	assert task.start_time == time(8, 0)
	assert app_test.session_state["schedule"]["tasks"] == [task]
	assert len(app_test.table) == 3
	assert "Scheduled" in str(app_test.table[-1].value)
	assert app_test.success[-1].value == "No overlapping tasks found in this schedule."


def test_schedule_conflict_warning_shows_tasks_and_times(monkeypatch) -> None:
	def create_overlapping_schedule(
		self, owner, pet, start_time, time_budget_minutes, schedule_date=None
	):
		walk_task, medication_task = pet.tasks
		walk_task.scheduled = True
		walk_task.start_time = time(8, 0)
		walk_task.end_time = time(8, 30)
		medication_task.scheduled = True
		medication_task.start_time = time(8, 20)
		medication_task.end_time = time(8, 30)
		return [medication_task, walk_task]

	monkeypatch.setattr(Scheduler, "create_daily_schedule", create_overlapping_schedule)
	app_path = Path(__file__).resolve().parents[1] / "app.py"
	app_test = AppTest.from_file(str(app_path)).run()
	pet = Pet("Mochi", "dog")
	pet.add_task(Task("Morning walk", 30, "high"))
	pet.add_task(Task("Medication", 10, "high"))
	owner = Owner("Jordan", pets=[pet])
	app_test.session_state["owner"] = owner
	app_test.run()

	app_test.button(key="generate_schedule").click().run()
	assert not app_test.exception
	assert [task.title for task in app_test.session_state["schedule"]["tasks"]] == [
		"Morning walk",
		"Medication",
	]
	warning = str(app_test.warning[0].value)
	assert "Mochi's Morning walk (08:00-08:30)" in warning
	assert "Mochi's Medication (08:20-08:30)" in warning
	assert "adjust one task if needed" in warning