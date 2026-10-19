# import classes from pawpal_system.py
from pawpal_system import Task, Pet, Owner, ScheduledItem, Scheduler
from datetime import time

# create an owner and at least two pets
owner= Owner("Anthony", "Mornings preferred", 360)

brody = Pet("Brody", "M", "Cat")
bentley = Pet("Bentley", "M", "Dog")

owner.add_pet(brody)
owner.add_pet(bentley)

# add tasks deliberately out of time order
bentley.add_task(Task("Give insulin shot", "medical", 5, 3, time(9, 30)))
brody.add_task(Task("Play with laser", "enrichment", 20, 1, time(18, 0)))
bentley.add_task(Task("Walk", "routine", 15, 1, time(8, 0)))
brody.add_task(Task("Feed", "routine", 10, 2, time(7, 30)))
bentley.add_task(Task("Brush teeth", "grooming", 5, 1, time(20, 15)))

scheduler = Scheduler(owner)


def pet_of(task):
    return next(p.name for p in owner.pets if task in p.tasks)


def show(title, tasks):
    print(f"\n{title}")
    print("-" * 40)
    if not tasks:
        print("(none)")
    for t in tasks:
        status = "done" if t.is_complete else "pending"
        print(f"{t.due_time:%H:%M} {pet_of(t)}: {t.name} [{status}]")


# mark a couple of tasks complete so the status filter has something to show
scheduler.filter_tasks(pet_name="Brody")[1].mark_complete()  # Feed
scheduler.filter_tasks(pet_name="Bentley")[1].mark_complete()  # Walk

# recurring demo: completing a daily task spawns tomorrow's copy
brody.add_task(Task("Evening meds", "medical", 5, 3, time(19, 0), frequency="daily"))
meds = brody.tasks[-1]
nxt = scheduler.mark_task_complete(meds)
print(f"Completed '{meds.name}' (due {meds.due_date}); next due {nxt.due_date}")

show("All tasks (insertion order)", scheduler.get_all_tasks())
show("All tasks sorted by time", scheduler.sort_by_time())
show("Pending tasks", scheduler.filter_tasks(is_complete=False))
show("Completed tasks", scheduler.filter_tasks(is_complete=True))
show("Bentley's tasks, sorted by time", scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Bentley")))
show("Brody's pending tasks, sorted by time", scheduler.sort_by_time(scheduler.filter_tasks(is_complete=False, pet_name="Brody")))

# conflict demo: two tasks at the same time, for different pets and for the same pet
bentley.add_task(Task("Vet call", "medical", 30, 2, time(14, 0)))
brody.add_task(Task("Nail trim", "grooming", 15, 1, time(14, 0)))
brody.add_task(Task("Brush fur", "grooming", 10, 1, time(14, 10)))

print("\nConflict check")
print("-" * 40)
conflicts = scheduler.find_conflicts()
for warning in conflicts:
    print(warning)
if not conflicts:
    print("No conflicts found")

# prints a "Today's Schedule" to the terminal.
items = scheduler.schedule_task()

print("\nToday's Schedule")
print("-" * 40)
for item in items:
    print(f"{item.time_slot} {item.pet_name}: {item.task.name} (priority {item.task.priority})")
