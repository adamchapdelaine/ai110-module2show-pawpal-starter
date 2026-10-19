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


```Today's Schedule
----------------------------------------
07:30-07:35 Bentley: Give insulin shot (priority 3)
07:35-07:45 Brody: Feed (priority 2)
07:45-08:00 Bentley: Walk (priority 1)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## Implementation Summary
So far, I've built a small scheduling system with five classes (Owner, Pet, Task, Scheduler, ScheduledItem).

Task represents a care activity the owner does for the pet. It holds a name, category, duration, priority, due time, frequency, and a completion flag.
Pet has a name, sex and species, and owns a list of Tasks as well as methods to add or remove them.
Owner has a name, preferences, available time, and owns a list of Pets.
Scheduler holds an Owner and produces the schedule.
ScheduledItem is an extra class I made to hold a record of the output of Scheduler, with a time slot string, the task, and the pet's name the task is assigned to.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Scheduler.get_todays_tasks() pulls all tasks through the owner and keeps the incomplete ones. It sorts them by due time, then by highest priority.
2. Scheduler.schedule_task() re-sorts those tasks by priority first, then due time. It starts the clock at the earliest due time, or 8:00 if there are no tasks.
3. It places tasks back to back and skips any task that no longer fits in the owner's remaining available minutes.
4. Each placed task becomes a ScheduledItem, with the pet name looked up from which pet owns the task.
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
