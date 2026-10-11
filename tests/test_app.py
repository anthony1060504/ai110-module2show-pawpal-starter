from datetime import time
from pathlib import Path

from streamlit.testing.v1 import AppTest


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