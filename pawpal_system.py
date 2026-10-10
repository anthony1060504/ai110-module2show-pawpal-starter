from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Owner:
    """Owner details and soft preferences, such as a preferred walk time."""

    name: str
    preferences: list[str] = field(default_factory=list)

    def update_preferences(self, preferences: list[str]) -> None:
        raise NotImplementedError


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        raise NotImplementedError

    def remove_task(self, task: CareTask) -> None:
        raise NotImplementedError


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: str


class Scheduler:
    def create_daily_plan(
        self,
        owner: Owner,
        pet: Pet,
        start_time: time,
        time_budget_minutes: int,
    ) -> DailyPlan:
        """Create today's plan, starting at start_time.

        Treat time_budget_minutes as the maximum task time available from
        start_time. The usable window is also limited by the time remaining
        before midnight. Schedule higher-priority tasks first; use preferences
        only to guide ordering among tasks of equal priority. Record tasks that
        do not fit in DailyPlan.notes.
        """
        raise NotImplementedError


@dataclass
class DailyPlan:
    plan_date: date
    items: list[PlanItem] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def add_item(self, item: PlanItem) -> None:
        raise NotImplementedError

    def get_total_planned_minutes(self) -> int:
        raise NotImplementedError


@dataclass
class PlanItem:
    task: CareTask
    start_time: time
    end_time: time
    reason: str