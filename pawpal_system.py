from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import List


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: int
    due_time: time
    is_complete: bool = False
    frequency: str = "once"
    description: str = ""

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_complete = True


@dataclass
class Pet:
    name: str
    sex: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list if it is present."""
        if task in self.tasks:
            self.tasks.remove(task)


@dataclass
class Owner:
    name: str
    preferences: str
    time_available_minutes: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's list if it is present."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class ScheduledItem:
    time_slot: str
    task: Task
    pet_name: str


@dataclass
class Scheduler:
    owner: Owner
    scheduled_items: List[ScheduledItem] = field(default_factory=list)

    def get_all_tasks(self) -> List[Task]:
        """Return every task belonging to the owner's pets."""
        return self.owner.get_all_tasks()

    def get_todays_tasks(self) -> List[Task]:
        """Return incomplete tasks sorted by due time, then highest priority first."""
        pending = [task for task in self.get_all_tasks() if not task.is_complete]
        return sorted(pending, key=lambda t: (t.due_time, -t.priority))

    def schedule_task(self) -> List[ScheduledItem]:
        """Build a priority-ordered schedule that fits within the owner's available time."""
        pet_names = {id(task): pet.name for pet in self.owner.pets for task in pet.tasks}
        by_priority = sorted(
            self.get_todays_tasks(), key=lambda t: (-t.priority, t.due_time)
        )

        start = min((t.due_time for t in by_priority), default=time(8, 0))
        current = datetime.combine(datetime.today(), start)
        minutes_left = self.owner.time_available_minutes

        self.scheduled_items = []
        for task in by_priority:
            if task.duration_minutes > minutes_left:
                continue
            end = current + timedelta(minutes=task.duration_minutes)
            slot = f"{current:%H:%M}-{end:%H:%M}"
            self.scheduled_items.append(
                ScheduledItem(slot, task, pet_names[id(task)])
            )
            minutes_left -= task.duration_minutes
            current = end
        return self.scheduled_items
