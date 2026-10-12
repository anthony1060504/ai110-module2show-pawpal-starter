from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta


@dataclass
class Owner:
	name: str
	preferences: list[str] = field(default_factory=list)
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this owner's collection."""
		self.pets.append(pet)

	def update_preferences(self, preferences: list[str]) -> None:
		"""Replace this owner's scheduling preferences."""
		self.preferences = list(preferences)

	def filter_tasks(
		self,
		pet_name: str | None = None,
		completed: bool | None = None,
	) -> list[Task]:
		"""Filter tasks by exact pet name and/or completion status.

		Pet-name matching ignores case and surrounding whitespace. When both
		filters are supplied, both must match. Results preserve pet and task order.
		"""
		normalized_name = pet_name.strip().casefold() if pet_name is not None else None
		return [
			task
			for pet in self.pets
			if normalized_name is None or pet.name.casefold() == normalized_name
			for task in pet.tasks
			if completed is None or task.completed == completed
		]


@dataclass
class Pet:
	name: str
	species: str
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a task to this pet's task list."""
		self.tasks.append(task)

	def remove_task(self, task: Task) -> None:
		"""Remove a task from this pet's task list."""
		self.tasks.remove(task)

	def mark_task_complete(self, task: Task, today: date | None = None) -> Task | None:
		"""Complete this pet's task and append its next occurrence, if recurring.

		Returns the new task, or None for one-time/already-completed tasks.
		Raises ValueError if the task is not in this pet's task list.
		"""
		if not any(existing_task is task for existing_task in self.tasks):
			raise ValueError("task does not belong to this pet")

		next_occurrence = task.mark_complete(today)
		if next_occurrence is not None:
			self.add_task(next_occurrence)
		return next_occurrence


@dataclass
class Task:
	title: str
	duration_minutes: int
	priority: str
	scheduled: bool = False
	start_time: time | None = None
	end_time: time | None = None
	reason: str = ""
	completed: bool = False
	frequency: str = "once"
	due_date: date = field(default_factory=date.today)

	def __post_init__(self) -> None:
		"""Normalize frequency and reject values other than once, daily, weekly."""
		self.frequency = self.frequency.strip().casefold()
		if self.frequency not in {"once", "daily", "weekly"}:
			raise ValueError("frequency must be 'once', 'daily', or 'weekly'")

	def mark_complete(self, today: date | None = None) -> Task | None:
		"""Mark this task complete and return a fresh next occurrence, if any.

		Daily tasks recur one day after ``today``; weekly tasks recur seven days
		later. One-time or already-completed tasks return None. This method does
		not add the new occurrence to a pet; use Pet.mark_task_complete for that.
		"""
		if self.completed:
			return None

		self.completed = True
		if self.frequency == "once":
			return None

		interval_days = 1 if self.frequency == "daily" else 7
		next_due_date = (today or date.today()) + timedelta(days=interval_days)
		return Task(
			title=self.title,
			duration_minutes=self.duration_minutes,
			priority=self.priority,
			frequency=self.frequency,
			due_date=next_due_date,
		)


class Scheduler:
	def sort_by_time(self, tasks: list[Task]) -> list[Task]:
		"""Return a stable chronological copy, placing tasks without a start last.

		Tasks with equal start times retain their input order; the input list is
		not modified.
		"""
		return sorted(
			tasks,
			key=lambda task: (
				task.start_time is None,
				task.start_time or time.min,
			),
		)

	def detect_conflicts(self, pets: list[Pet]) -> list[str]:
		"""Return warnings for overlapping intervals across the supplied pets.

		Only scheduled, incomplete tasks with both times set are compared. Strict
		interval overlap is used, so adjacent tasks are not conflicts. Warnings
		are returned without raising or rescheduling tasks.
		"""
		scheduled_tasks = [
			(pet, task)
			for pet in pets
			for task in pet.tasks
			if task.scheduled
			and not task.completed
			and task.start_time is not None
			and task.end_time is not None
		]
		warnings = []

		for index, (pet, task) in enumerate(scheduled_tasks):
			start_time = task.start_time
			end_time = task.end_time
			if start_time is None or end_time is None:
				continue

			for other_pet, other_task in scheduled_tasks[index + 1 :]:
				other_start = other_task.start_time
				other_end = other_task.end_time
				if other_start is None or other_end is None:
					continue
				if start_time < other_end and other_start < end_time:
					warnings.append(
						f"Warning: {pet.name}'s {task.title} "
						f"({start_time:%H:%M}-{end_time:%H:%M}) overlaps with "
						f"{other_pet.name}'s {other_task.title} "
						f"({other_start:%H:%M}-{other_end:%H:%M})."
					)

		return warnings

	def create_daily_schedule(
		self,
		owner: Owner,
		pet: Pet,
		start_time: time,
		time_budget_minutes: int,
		schedule_date: date | None = None,
	) -> list[Task]:
		"""Schedule eligible tasks for one pet within the budget and before midnight.

		Completed tasks and tasks due after ``schedule_date`` remain in the
		returned list but are not scheduled. Eligible tasks are ordered by
		priority, then owner preference, then original pet-list order. Tasks that
		do not fit remain unscheduled with a reason.
		"""
		if time_budget_minutes < 0:
			raise ValueError("time_budget_minutes cannot be negative")
		if any(task.duration_minutes < 0 for task in pet.tasks):
			raise ValueError("task durations cannot be negative")
		date_to_schedule = schedule_date or date.today()

		priority_order = {"high": 0, "medium": 1, "low": 2}
		preferred_titles = {preference.casefold() for preference in owner.preferences}
		ordered_tasks = sorted(
			enumerate(pet.tasks),
			key=lambda indexed_task: (
				priority_order.get(indexed_task[1].priority.casefold(), 3),
				indexed_task[1].title.casefold() not in preferred_titles,
				indexed_task[0],
			),
		)

		day = date(2000, 1, 1)
		schedule_start = datetime.combine(day, start_time)
		midnight = datetime.combine(day + timedelta(days=1), time.min)
		budget_end = schedule_start + timedelta(minutes=time_budget_minutes)
		schedule_end = min(midnight, budget_end)
		current_time = schedule_start

		for _, task in ordered_tasks:
			task.scheduled = False
			task.start_time = None
			task.end_time = None
			task.reason = ""
			if task.completed:
				task.reason = "Task has already been completed."
				continue
			if task.due_date > date_to_schedule:
				task.reason = f"Not due until {task.due_date.isoformat()}."
				continue

			task_end = current_time + timedelta(minutes=task.duration_minutes)
			if task_end <= schedule_end:
				task.scheduled = True
				task.start_time = current_time.time()
				task.end_time = task_end.time()
				current_time = task_end
			elif budget_end < midnight:
				task.reason = "Does not fit within the available time budget."
			else:
				task.reason = "Does not fit before midnight."

		return self.sort_by_time([task for _, task in ordered_tasks])
