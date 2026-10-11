from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_updates_task_status() -> None:
	task = Task("Morning walk", 20, "high")

	assert not task.completed

	task.mark_complete()

	assert task.completed


def test_add_task_increases_pet_task_count() -> None:
	pet = Pet("Mochi", "dog")
	task = Task("Feeding", 10, "high")

	assert len(pet.tasks) == 0

	pet.add_task(task)

	assert len(pet.tasks) == 1


def test_add_pet_increases_owner_pet_count() -> None:
	owner = Owner("Jordan")
	pet = Pet("Mochi", "dog")

	owner.add_pet(pet)

	assert owner.pets == [pet]


def test_schedule_orders_tasks_and_respects_time_budget() -> None:
	owner = Owner("Jordan")
	pet = Pet("Mochi", "dog")
	low_priority_task = Task("Feeding", 10, "low")
	high_priority_task = Task("Morning walk", 20, "high")
	pet.add_task(low_priority_task)
	pet.add_task(high_priority_task)

	scheduled_tasks = Scheduler().create_daily_schedule(owner, pet, time(8, 0), 25)

	assert scheduled_tasks == [high_priority_task, low_priority_task]
	assert high_priority_task.scheduled
	assert high_priority_task.start_time == time(8, 0)
	assert high_priority_task.end_time == time(8, 20)
	assert not low_priority_task.scheduled
	assert low_priority_task.reason == "Does not fit within the available time budget."