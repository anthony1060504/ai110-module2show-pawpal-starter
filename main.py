from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan", preferences=["Morning walk"])
    biscuit = Pet("Biscuit", "Golden Retriever")
    whiskers = Pet("Whiskers", "Cat")
    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    biscuit.add_task(Task("Breakfast", 10, "high"))
    biscuit.add_task(Task("Morning walk", 30, "high"))
    biscuit.add_task(Task("Training", 15, "medium"))

    whiskers.add_task(Task("Breakfast", 10, "high"))
    whiskers.add_task(Task("Playtime", 20, "medium"))
    whiskers.add_task(Task("Grooming", 15, "low"))

    scheduler = Scheduler()
    print("Today's Schedule")
    print(f"Owner: {owner.name}")

    for pet in owner.pets:
        tasks = scheduler.create_daily_schedule(
            owner,
            pet,
            start_time=time(8, 0),
            time_budget_minutes=60,
        )
        print(f"\n{pet.name} ({pet.species})")

        for task in tasks:
            if task.scheduled:
                print(
                    f"  {task.start_time:%H:%M}-{task.end_time:%H:%M} | "
                    f"{task.title} ({task.duration_minutes} min, {task.priority})"
                )
            else:
                print(f"  Not scheduled | {task.title}: {task.reason}")


if __name__ == "__main__":
    main()
