from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time


@dataclass
class Owner:
	name: str
	preferences: list[str] = field(default_factory=list)
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		raise NotImplementedError

	def update_preferences(self, preferences: list[str]) -> None:
		raise NotImplementedError


@dataclass
class Pet:
	name: str
	species: str
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		raise NotImplementedError

	def remove_task(self, task: Task) -> None:
		raise NotImplementedError


@dataclass
class Task:
	title: str
	duration_minutes: int
	priority: str
	scheduled: bool = False
	start_time: time | None = None
	end_time: time | None = None
	reason: str = ""


class Scheduler:
	def create_daily_schedule(
		self,
		owner: Owner,
		pet: Pet,
		start_time: time,
		time_budget_minutes: int,
	) -> list[Task]:
		raise NotImplementedError
