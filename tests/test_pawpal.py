from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_updates_task_status() -> None:
	task = Task("Morning walk", 20, "high")

	assert not task.completed

	task.mark_complete()

	assert task.completed


def test_pet_completion_creates_daily_occurrence_for_next_day() -> None:
	today = date(2026, 10, 11)
	pet = Pet("Mochi", "dog")
	task = Task("Medication", 5, "high", frequency="daily", due_date=today)
	pet.add_task(task)

	next_occurrence = pet.mark_task_complete(task, today)

	assert task.completed
	assert next_occurrence is not None
	assert next_occurrence.due_date == date(2026, 10, 12)
	assert next_occurrence.frequency == "daily"
	assert not next_occurrence.completed
	assert pet.tasks == [task, next_occurrence]


def test_pet_completion_does_not_repeat_completed_recurring_task() -> None:
	today = date(2026, 10, 11)
	pet = Pet("Mochi", "dog")
	task = Task("Medication", 5, "high", frequency="daily", due_date=today)
	pet.add_task(task)

	first_occurrence = pet.mark_task_complete(task, today)
	second_occurrence = pet.mark_task_complete(task, today)

	assert first_occurrence is not None
	assert second_occurrence is None
	assert pet.tasks == [task, first_occurrence]


def test_pet_completion_creates_weekly_occurrence_seven_days_later() -> None:
	today = date(2026, 10, 11)
	pet = Pet("Mochi", "dog")
	task = Task("Grooming", 30, "medium", frequency="weekly", due_date=today)
	pet.add_task(task)

	next_occurrence = pet.mark_task_complete(task, today)

	assert next_occurrence is not None
	assert next_occurrence.due_date == date(2026, 10, 18)
	assert next_occurrence.frequency == "weekly"
	assert pet.tasks == [task, next_occurrence]


def test_pet_completion_does_not_repeat_one_time_task() -> None:
	pet = Pet("Mochi", "dog")
	task = Task("Vet visit", 60, "high")
	pet.add_task(task)

	assert pet.mark_task_complete(task, date(2026, 10, 11)) is None
	assert task.completed
	assert pet.tasks == [task]


def test_scheduler_excludes_future_and_completed_tasks() -> None:
	today = date(2026, 10, 11)
	owner = Owner("Jordan")
	pet = Pet("Mochi", "dog")
	future_task = Task(
		"Medication",
		5,
		"high",
		frequency="daily",
		due_date=date(2026, 10, 12),
	)
	completed_task = Task("Vet visit", 30, "medium", completed=True, due_date=today)
	pet.add_task(future_task)
	pet.add_task(completed_task)

	tasks = Scheduler().create_daily_schedule(
		owner,
		pet,
		time(8, 0),
		60,
		schedule_date=today,
	)

	assert tasks == [future_task, completed_task]
	assert not future_task.scheduled
	assert future_task.reason == "Not due until 2026-10-12."
	assert not completed_task.scheduled
	assert completed_task.reason == "Task has already been completed."

	due_date_tasks = Scheduler().create_daily_schedule(
		owner,
		pet,
		time(8, 0),
		60,
		schedule_date=date(2026, 10, 12),
	)

	assert future_task in due_date_tasks
	assert future_task.scheduled
	assert future_task.start_time == time(8, 0)


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


def test_filter_tasks_by_completion_status() -> None:
	owner = Owner("Jordan")
	pet = Pet("Mochi", "dog")
	completed_task = Task("Breakfast", 10, "high", completed=True)
	incomplete_task = Task("Walk", 20, "high")
	pet.add_task(completed_task)
	pet.add_task(incomplete_task)
	owner.add_pet(pet)

	assert owner.filter_tasks(completed=True) == [completed_task]
	assert owner.filter_tasks(completed=False) == [incomplete_task]


def test_filter_tasks_by_pet_name_case_insensitively() -> None:
	owner = Owner("Jordan")
	mochi = Pet("Mochi", "dog")
	mochi_task = Task("Walk", 20, "high")
	mochi.add_task(mochi_task)
	pepper = Pet("Pepper", "cat")
	pepper_task = Task("Feeding", 10, "medium")
	pepper.add_task(pepper_task)
	owner.add_pet(mochi)
	owner.add_pet(pepper)

	assert owner.filter_tasks(pet_name="mOcHi") == [mochi_task]
	assert owner.filter_tasks(pet_name="Moch") == []


def test_filter_tasks_combines_pet_name_and_completion_filters() -> None:
	owner = Owner("Jordan")
	pet = Pet("Mochi", "dog")
	completed_task = Task("Breakfast", 10, "high", completed=True)
	incomplete_task = Task("Walk", 20, "high")
	pet.add_task(completed_task)
	pet.add_task(incomplete_task)
	owner.add_pet(pet)

	assert owner.filter_tasks(pet_name="Mochi", completed=False) == [incomplete_task]
	assert owner.filter_tasks() == [completed_task, incomplete_task]


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


def test_schedule_with_no_tasks_returns_empty_list() -> None:
	tasks = Scheduler().create_daily_schedule(
		Owner("Jordan"), Pet("Mochi", "dog"), time(8, 0), 60
	)

	assert tasks == []


def test_schedule_allows_tasks_to_fill_budget_exactly() -> None:
	owner = Owner("Jordan")
	pet = Pet("Mochi", "dog")
	first_task = Task("Breakfast", 20, "high")
	second_task = Task("Walk", 10, "high")
	pet.add_task(first_task)
	pet.add_task(second_task)

	tasks = Scheduler().create_daily_schedule(owner, pet, time(8, 0), 30)

	assert tasks == [first_task, second_task]
	assert first_task.start_time == time(8, 0)
	assert first_task.end_time == time(8, 20)
	assert second_task.start_time == time(8, 20)
	assert second_task.end_time == time(8, 30)
	assert first_task.scheduled
	assert second_task.scheduled


def test_schedule_does_not_schedule_tasks_past_midnight() -> None:
	today = date(2026, 10, 11)
	owner = Owner("Jordan")
	pet = Pet("Mochi", "dog")
	first_task = Task("Late walk", 10, "high", due_date=today)
	second_task = Task("Late snack", 5, "high", due_date=today)
	pet.add_task(first_task)
	pet.add_task(second_task)

	tasks = Scheduler().create_daily_schedule(
		owner, pet, time(23, 50), 30, schedule_date=today
	)

	assert tasks == [first_task, second_task]
	assert first_task.scheduled
	assert first_task.start_time == time(23, 50)
	assert first_task.end_time == time(0, 0)
	assert not second_task.scheduled
	assert second_task.reason == "Does not fit before midnight."


def test_schedule_prefers_owner_preference_for_equal_priority_tasks() -> None:
	owner = Owner("Jordan", preferences=["walk"])
	pet = Pet("Mochi", "dog")
	other_task = Task("Feeding", 10, "high")
	preferred_task = Task("Walk", 10, "high")
	pet.add_task(other_task)
	pet.add_task(preferred_task)

	tasks = Scheduler().create_daily_schedule(owner, pet, time(8, 0), 20)

	assert tasks == [preferred_task, other_task]
	assert preferred_task.start_time == time(8, 0)
	assert other_task.start_time == time(8, 10)


def test_sort_by_time_orders_tasks_and_keeps_unscheduled_last() -> None:
	scheduler = Scheduler()
	late_task = Task("Playtime", 20, "medium", start_time=time(9, 0))
	early_task = Task("Breakfast", 10, "high", start_time=time(8, 0))
	unscheduled_task = Task("Grooming", 15, "low")
	tasks = [late_task, unscheduled_task, early_task]

	result = scheduler.sort_by_time(tasks)

	assert result == [early_task, late_task, unscheduled_task]
	assert tasks == [late_task, unscheduled_task, early_task]
	assert result is not tasks


def test_sort_by_time_preserves_order_for_matching_start_times() -> None:
	scheduler = Scheduler()
	first_task = Task("First", 10, "high", start_time=time(8, 0))
	second_task = Task("Second", 10, "high", start_time=time(8, 0))

	assert scheduler.sort_by_time([first_task, second_task]) == [first_task, second_task]


def test_detect_conflicts_reports_overlapping_tasks_for_same_pet() -> None:
	scheduler = Scheduler()
	pet = Pet("Mochi", "dog")
	pet.add_task(
		Task(
			"Walk",
			30,
			"high",
			scheduled=True,
			start_time=time(8, 0),
			end_time=time(8, 30),
		)
	)
	pet.add_task(
		Task(
			"Medication",
			10,
			"high",
			scheduled=True,
			start_time=time(8, 20),
			end_time=time(8, 30),
		)
	)

	warnings = scheduler.detect_conflicts([pet])

	assert len(warnings) == 1
	assert "Mochi's Walk (08:00-08:30)" in warnings[0]
	assert "Mochi's Medication (08:20-08:30)" in warnings[0]


def test_detect_conflicts_reports_tasks_with_identical_times() -> None:
	scheduler = Scheduler()
	pet = Pet("Mochi", "dog")
	pet.add_task(
		Task(
			"Walk",
			30,
			"high",
			scheduled=True,
			start_time=time(8, 0),
			end_time=time(8, 30),
		)
	)
	pet.add_task(
		Task(
			"Medication",
			30,
			"high",
			scheduled=True,
			start_time=time(8, 0),
			end_time=time(8, 30),
		)
	)

	warnings = scheduler.detect_conflicts([pet])

	assert len(warnings) == 1
	assert "Mochi's Walk (08:00-08:30)" in warnings[0]
	assert "Mochi's Medication (08:00-08:30)" in warnings[0]


def test_detect_conflicts_reports_overlaps_across_pets() -> None:
	scheduler = Scheduler()
	biscuit = Pet("Biscuit", "dog")
	whiskers = Pet("Whiskers", "cat")
	biscuit.add_task(
		Task(
			"Walk",
			30,
			"high",
			scheduled=True,
			start_time=time(8, 0),
			end_time=time(8, 30),
		)
	)
	whiskers.add_task(
		Task(
			"Breakfast",
			10,
			"high",
			scheduled=True,
			start_time=time(8, 15),
			end_time=time(8, 25),
		)
	)

	warnings = scheduler.detect_conflicts([biscuit, whiskers])

	assert len(warnings) == 1
	assert "Biscuit's Walk" in warnings[0]
	assert "Whiskers's Breakfast" in warnings[0]


def test_detect_conflicts_ignores_adjacent_unscheduled_and_completed_tasks() -> None:
	scheduler = Scheduler()
	pet = Pet("Mochi", "dog")
	pet.add_task(
		Task(
			"Walk",
			30,
			"high",
			scheduled=True,
			start_time=time(8, 0),
			end_time=time(8, 30),
		)
	)
	pet.add_task(
		Task(
			"Breakfast",
			10,
			"high",
			scheduled=True,
			start_time=time(8, 30),
			end_time=time(8, 40),
		)
	)
	pet.add_task(
		Task(
			"Completed task",
			10,
			"medium",
			scheduled=True,
			start_time=time(8, 15),
			end_time=time(8, 25),
			completed=True,
		)
	)
	pet.add_task(
		Task(
			"Unscheduled task",
			10,
			"medium",
			start_time=time(8, 15),
			end_time=time(8, 25),
		)
	)

	assert scheduler.detect_conflicts([pet]) == []