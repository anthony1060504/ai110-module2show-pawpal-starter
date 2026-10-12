from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan", preferences=["Morning walk"])
    biscuit = Pet("Biscuit", "Golden Retriever")
    whiskers = Pet("Whiskers", "Cat")
    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    biscuit_training = Task("Training", 15, "medium")
    biscuit.add_task(biscuit_training)
    biscuit.add_task(Task("Breakfast", 10, "high"))
    biscuit.add_task(Task("Morning walk", 30, "high"))

    whiskers.add_task(Task("Grooming", 15, "low"))
    whiskers.add_task(Task("Playtime", 20, "medium"))
    whiskers.add_task(Task("Breakfast", 10, "high"))

    scheduler = Scheduler()
    print("Today's Schedule")
    print(f"Owner: {owner.name}")

    for pet in owner.pets:
        schedule_start = time(8, 0) if pet is biscuit else time(8, 45)
        tasks = scheduler.create_daily_schedule(
            owner,
            pet,
            start_time=schedule_start,
            time_budget_minutes=60,
        )
        tasks = scheduler.sort_by_time(tasks)
        print(f"\n{pet.name} ({pet.species})")

        for task in tasks:
            if task.scheduled:
                print(
                    f"  {task.start_time:%H:%M}-{task.end_time:%H:%M} | "
                    f"{task.title} ({task.duration_minutes} min, {task.priority})"
                )
            else:
                print(f"  Not scheduled | {task.title}: {task.reason}")

    conflict_warnings = scheduler.detect_conflicts(owner.pets)
    print("\nConflict warnings")
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"  {warning}")
    else:
        print("  None")

    biscuit_training.mark_complete()
    completed_tasks = owner.filter_tasks(completed=True)
    incomplete_biscuit_tasks = owner.filter_tasks(
        pet_name=biscuit.name,
        completed=False,
    )

    print("\nTask filters (after marking Training complete)")
    print("Completed tasks")
    for task in scheduler.sort_by_time(completed_tasks):
        print(f"  {task.title} (Biscuit)")

    print("\nIncomplete tasks for Biscuit")
    for task in scheduler.sort_by_time(incomplete_biscuit_tasks):
        if task.scheduled:
            print(f"  {task.start_time:%H:%M} | {task.title}")
        else:
            print(f"  Not scheduled | {task.title}")


if __name__ == "__main__":
    main()
