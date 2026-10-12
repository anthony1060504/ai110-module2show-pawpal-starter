# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
Owner: Jordan

Biscuit (Golden Retriever)
  08:00-08:30 | Morning walk (30 min, high)
  08:30-08:40 | Breakfast (10 min, high)
  08:40-08:55 | Training (15 min, medium)

Whiskers (Cat)
  08:00-08:10 | Breakfast (10 min, high)
  08:10-08:30 | Playtime (20 min, medium)
  08:30-08:45 | Grooming (15 min, low)
```
```
Today's Schedule
Owner: Jordan

Biscuit (Golden Retriever)
  08:00-08:30 | Morning walk (30 min, high)
  08:30-08:40 | Breakfast (10 min, high)
  08:40-08:55 | Training (15 min, medium)

Whiskers (Cat)
  08:00-08:10 | Breakfast (10 min, high)
  08:10-08:30 | Playtime (20 min, medium)
  08:30-08:45 | Grooming (15 min, low)

Task filters (after marking Training complete)
Completed tasks
  Training (Biscuit)

Incomplete tasks for Biscuit
  08:00 | Morning walk
  08:30 | Breakfast
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

```
The PawPal tests cover task completion and recurrence, owner/pet task management and filtering, schedule eligibility and priority, time-budget and midnight boundaries, chronological sorting, and conflict detection, including duplicate intervals.
```

Sample test output:

```
(.venv) PS C:\Users\antho\ai110-module1show-gameglitchinvestigator-starter\ai110-module2show-pawpal-starter> python -m pytest
=================================================================== test session starts ====================================================================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\antho\ai110-module1show-gameglitchinvestigator-starter\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 23 items

tests\test_app.py .                                                                                                                                   [  4%]
tests\test_pawpal.py ......................                                                                                                           [100%]

==================================================================== 23 passed in 1.11s ====================================================================
```

```
Confidence: 4/5 stars. All 23 tests passed, including the app test. The result supports confidence in the covered behaviors, though it cannot guarantee reliability for untested cases.
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time(tasks)` | Returns a stable chronological copy; tasks without a start time appear last. `Scheduler.create_daily_schedule(...)` selects tasks by priority, then owner preference, then original order. |

| Filtering | `Owner.filter_tasks(pet_name=None, completed=None)` | Filters by exact, case-insensitive pet name and/or completion status; supplied filters are combined, and original pet/task order is preserved. |

| Conflict detection | `Scheduler.detect_conflicts(pets)` | Checks scheduled, incomplete tasks with start and end times for overlapping intervals. Returns warning messages; adjacent intervals are allowed and schedules are not changed. |

| Recurring tasks | `Task.__post_init__()`, `Task.mark_complete(today=None)`, `Pet.mark_task_complete(task, today=None)` | Supports `once`, `daily`, and `weekly` frequency. Completing a daily or weekly task creates a fresh occurrence due one or seven days later; `Pet.mark_task_complete` adds it to the pet's task list. |

| Due-date scheduling | `Scheduler.create_daily_schedule(..., schedule_date=None)` | Excludes completed tasks and tasks due after the selected schedule date, retaining excluded tasks with a reason. Applies task durations within the time budget and midnight limit. |


## Features

- **Priority- and preference-aware planning:** Schedules eligible tasks by priority, uses owner preferences to break priority ties, and preserves task order for remaining ties.
- **Time and due-date constraints:** Fits task durations within the available time budget and before midnight. Completed, not-yet-due, or over-budget tasks remain visible with an explanation.
- **Chronological sorting:** Displays tasks by start time, with unscheduled tasks last; equal start times retain their original order.
- **Conflict warnings:** Warns when scheduled, incomplete tasks for the selected pet have overlapping time ranges. Adjacent tasks are allowed, and the app asks the owner to review the times rather than rescheduling automatically.
- **Task filtering:** Filters by pet name and completion status; pet-name matching ignores case and surrounding whitespace, and supplied filters are combined.
- **Recurring task support:** The task model supports one-time, daily, and weekly tasks. Completing a daily or weekly task creates a fresh occurrence due one or seven days later, and the pet adds that occurrence to its task list.


## 📸 Demo Walkthrough

PawPal+ lets an owner add pets, enter care tasks with durations and priorities, and generate a daily schedule from a chosen start time and time budget.

1. Enter the owner's name, add a pet and species, then add tasks such as walks, meals, or medication.
2. Choose the active pet and set the schedule start time and available time budget.
3. Select **Generate schedule** to view tasks in chronological order, including each task's status, start and end time, and an explanation when it could not be scheduled.
4. Review any overlap warning. The Streamlit app checks the selected pet's schedule and asks the owner to review conflicting times; it does not automatically reschedule tasks.
5. Run `python main.py` to see a two-pet CLI example. It also demonstrates cross-pet conflict detection and filtering after a task is marked complete.

The scheduler prioritizes tasks by priority, uses owner preferences to break priority ties, respects due dates and the time budget, and does not schedule tasks past midnight. Sorting is stable, with unscheduled tasks last. The CLI example below shows the overlap between Biscuit's Training and Whiskers' Breakfast.

```text
$ python main.py
Today's Schedule
Owner: Jordan

Biscuit (Golden Retriever)
  08:00-08:30 | Morning walk (30 min, high)
  08:30-08:40 | Breakfast (10 min, high)
  08:40-08:55 | Training (15 min, medium)

Whiskers (Cat)
  08:45-08:55 | Breakfast (10 min, high)
  08:55-09:15 | Playtime (20 min, medium)
  09:15-09:30 | Grooming (15 min, low)

Conflict warnings
  Warning: Biscuit's Training (08:40-08:55) overlaps with Whiskers's Breakfast (08:45-08:55).

Task filters (after marking Training complete)
Completed tasks
  Training (Biscuit)

Incomplete tasks for Biscuit
  08:00 | Morning walk
  08:30 | Breakfast
```


