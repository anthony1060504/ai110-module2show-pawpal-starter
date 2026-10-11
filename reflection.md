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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

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
