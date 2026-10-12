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
The PawPal tests cover task completion and recurrence, owner/pet task management and filtering, schedule eligibility and priority, time-budget and midnight boundaries, chronological sorting, and conflict detection, including duplicate intervals.

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

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time(tasks)` | Returns a stable chronological copy; tasks without a start time appear last. `Scheduler.create_daily_schedule(...)` selects tasks by priority, then owner preference, then original order. |

| Filtering | `Owner.filter_tasks(pet_name=None, completed=None)` | Filters by exact, case-insensitive pet name and/or completion status; supplied filters are combined, and original pet/task order is preserved. |

| Conflict detection | `Scheduler.detect_conflicts(pets)` | Checks scheduled, incomplete tasks with start and end times for overlapping intervals. Returns warning messages; adjacent intervals are allowed and schedules are not changed. |

| Recurring tasks | `Task.__post_init__()`, `Task.mark_complete(today=None)`, `Pet.mark_task_complete(task, today=None)` | Supports `once`, `daily`, and `weekly` frequency. Completing a daily or weekly task creates a fresh occurrence due one or seven days later; `Pet.mark_task_complete` adds it to the pet's task list. |

| Due-date scheduling | `Scheduler.create_daily_schedule(..., schedule_date=None)` | Excludes completed tasks and tasks due after the selected schedule date, retaining excluded tasks with a reason. Applies task durations within the time budget and midnight limit. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
