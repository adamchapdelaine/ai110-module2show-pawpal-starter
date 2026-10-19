# import classes from pawpal_system.py
from pawpal_system import Task, Pet, Owner, ScheduledItem, Scheduler
from datetime import time

# create an owner and at least two pets
owner= Owner("Anthony", "Mornings preferred", 360)

brody = Pet("Brody", "M", "Cat")
bentley = Pet("Bentley", "M", "Dog")

owner.add_pet(brody)
owner.add_pet(bentley)

# add at least three tasks with different times to those pets
bentley.add_task(Task("Walk", "routine", 15, 1, time(8, 0)))
bentley.add_task(Task("Give insulin shot", "medical", 5, 3, time(9, 30)))
brody.add_task(Task("Feed", "routine", 10, 2, time(7, 30)))

# prints a "Today's Schedule" to the terminal.
scheduler = Scheduler(owner)
items = scheduler.schedule_task()

print("Today's Schedule")
print("-" * 40)
for item in items:
    print(f"{item.time_slot} {item.pet_name}: {item.task.name} (priority {item.task.priority})")
