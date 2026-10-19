from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, datetime, time, timedelta
from typing import List



RECURRENCE_STEPS = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


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
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Task | None:
        """Mark this task as completed; return the next occurrence if it recurs."""
        self.is_complete = True
        return self.next_occurrence()

    def next_occurrence(self) -> Task | None:
        """Return a fresh, incomplete copy of this task for its next recurrence.

        Daily tasks come due one day from today and weekly tasks seven days from
        today (see RECURRENCE_STEPS). Returns None for non-recurring ("once") tasks.
        """
        step = RECURRENCE_STEPS.get(self.frequency.lower())
        if step is None:
            return None
        return replace(self, is_complete=False, due_date=date.today() + step)

    @property
    def start(self) -> datetime:
        """When the task begins."""
        return datetime.combine(self.due_date, self.due_time)

    @property
    def end(self) -> datetime:
        """When the task finishes."""
        return self.start + timedelta(minutes=self.duration_minutes)


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
        """Return today's workload: incomplete tasks due today or earlier (overdue).

        Results are sorted by due time, with higher priority first on ties.
        """
        today = date.today()
        pending = [
            task
            for task in self.get_all_tasks()
            if not task.is_complete and task.due_date <= today
        ]
        return sorted(pending, key=lambda t: (t.due_time, -t.priority))

    def mark_task_complete(self, task: Task) -> Task | None:
        """Complete a task and schedule its next occurrence if it recurs.

        For daily/weekly tasks, the new copy is added to the pet that owns the
        original task. Returns the new task, or None if the task does not recur.
        """
        next_task = task.mark_complete()
        if next_task is not None:
            for pet in self.owner.pets:
                if task in pet.tasks:
                    pet.add_task(next_task)
                    break
        return next_task

    def sort_by_time(self, tasks: List[Task] | None = None) -> List[Task]:
        """Return the given tasks (default: all tasks) sorted by due time, earliest first.

        Sorts on time of day only (due_time), not due_date. The input list is not
        modified.
        """
        if tasks is None:
            tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda t: t.due_time)

    def filter_tasks(
        self, is_complete: bool | None = None, pet_name: str | None = None
    ) -> List[Task]:
        """Return tasks matching the completion status and/or pet name.

        Each filter is optional; None means "don't filter on this". The pet name
        match is case-insensitive. Tasks keep their per-pet insertion order.
        """
        matches = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.tasks:
                if is_complete is None or task.is_complete == is_complete:
                    matches.append(task)
        return matches

    def find_conflicts(self) -> List[str]:
        """Return a warning message for each pair of pending tasks that overlap in time.

        Tasks (across all pets) are sorted by start time, then each is compared with
        the tasks after it until one starts at or after its end, since later tasks
        cannot overlap either. Back-to-back tasks are not conflicts. Warnings say
        whether the pair belongs to the same pet or different pets. Never raises:
        an empty list means no conflicts.
        """
        entries = sorted(
            ((t, pet.name) for pet in self.owner.pets for t in pet.tasks if not t.is_complete),
            key=lambda e: e[0].start,
        )
        warnings = []
        for i, (a, pet_a) in enumerate(entries):
            for b, pet_b in entries[i+1:]:
                if b.start >= a.end:
                    break # sorted by start, so nothing later can overlap `a`
                kind = "same pet" if pet_a == pet_b else "different pets"
                warnings.append(
                    f"Warning ({kind}): {pet_a}'s '{a.name}' at {a.due_time:%H:%M} "
                    f"overlaps {pet_b}'s '{b.name}' at {b.due_time:%H:%M}"
                )
        return warnings

    def schedule_task(self) -> List[ScheduledItem]:
        """Build a priority-ordered schedule that fits within the owner's available time.

        Greedy: today's tasks are sorted by priority (highest first), then packed back
        to back starting at the earliest due time. A task longer than the remaining
        time is skipped, and shorter ones after it may still fit. Each task's own
        due_time is not used as its slot, so the result never has overlaps.
        """
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
