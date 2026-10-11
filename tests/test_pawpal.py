from pawpal_system import Pet, Task


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