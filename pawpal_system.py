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

	def mark_complete(self) -> None:
		"""Mark this task as completed."""
		self.completed = True


class Scheduler:
	def create_daily_schedule(
		self,
		owner: Owner,
		pet: Pet,
		start_time: time,
		time_budget_minutes: int,
	) -> list[Task]:
		"""Create a prioritized schedule for one pet within the time budget."""
		if time_budget_minutes < 0:
			raise ValueError("time_budget_minutes cannot be negative")
		if any(task.duration_minutes < 0 for task in pet.tasks):
			raise ValueError("task durations cannot be negative")

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

		return [task for _, task in ordered_tasks]
