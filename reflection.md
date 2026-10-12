# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included four classes: Owner, Pet, Task, and Scheduler. Owner stores the owner’s name and preferences and can have multiple pets. Pet stores basic pet information and manages its tasks. Each Task stores its title, duration, and priority, along with its scheduling status, start and end times, and a reason. Scheduler creates a one-day schedule for a selected pet using the owner’s preferences, the start time, and the available time budget. Higher-priority tasks are scheduled first, preferences help order tasks with equal priority, and tasks that do not fit are marked with a reason. I kept the design simple by representing the schedule on the Task objects instead of adding separate plan classes.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. While translating the UML into the Python skeleton, I clarified the scheduler’s time constraints. I renamed `available_minutes` to `time_budget_minutes` to show that it applies from the selected start time, and specified that the schedule must also end by midnight. I also clarified that task priority sets the ordering, while owner preferences are soft tie-breakers for tasks with equal priority. These changes made the scheduler’s expected behavior less ambiguous before implementing its logic.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler treats the start time, time budget, and midnight as hard limits. Each task’s duration determines whether it fits; completed tasks and tasks not yet due are skipped, and tasks that do not fit are left unscheduled with a reason. Eligible tasks are ordered by priority high, medium, then low. Owner preferences only break ties between tasks at the same priority, so a preferred low-priority task does not jump ahead of a high-priority one. I chose this order to give important tasks first access to limited time while still letting preferences personalize the schedule. Schedules are built per pet, and cross-pet overlaps are reported as warnings rather than automatically rescheduled.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that the scheduler creates each pet’s schedule independently, so tasks can overlap across pets. It reports those overlaps as warnings instead of automatically moving tasks. This keeps scheduling simple and predictable, while letting the owner decide whether an overlap is actually a problem and which task to move.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI as a coding partner during design, implementation, and documentation. It helped me compare my initial UML with the finished classes, connect the Scheduler’s sorting and conflict detection to the Streamlit interface, add focused tests, and describe the app’s behavior in the README.

The most helpful prompts were specific and grounded in my code, such as asking whether the UML matched pawpal_system.py or how to present a detected conflict clearly to a pet owner. Asking for focused checks also helped: I verified the UI changes with tests and checked the README’s CLI example against main.py instead of relying on generated descriptions alone.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One decision was whether the app should warn about overlaps across pets. AI suggested retaining each pet’s schedule so the UI could compare them, but I chose to check only the selected pet’s newly generated schedule. The app stores one active schedule, so comparing other pets’ task times could rely on stale data. I checked the app’s session-state flow and tested both overlapping and non-overlapping schedules to verify that the warnings matched the current schedule.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task completion and recurrence, adding and removing pets’ tasks, owner filtering by pet and completion status, and scheduling behavior such as priority ordering, owner preferences, due dates, time budgets, and the midnight limit. I also tested chronological sorting and conflict detection, including overlaps, adjacent tasks, completed tasks, and unscheduled tasks. The Streamlit tests cover adding a pet and task, generating a schedule, and showing both conflict warnings and the no-conflict message.

These tests matter because they check the scheduling rules and the UI together, including boundary cases that could otherwise produce misleading times or warnings. The full suite passed with 24 tests.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
