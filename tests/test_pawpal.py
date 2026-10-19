from datetime import time

from pawpal_system import Pet, Task


def make_task() -> Task:
    return Task(
        name="Morning walk",
        category="exercise",
        duration_minutes=30,
        priority=3,
        due_time=time(8, 0),
    )


def test_mark_complete_changes_task_status():
    task = make_task()
    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", sex="male", species="dog")
    assert len(pet.tasks) == 0

    pet.add_task(make_task())

    assert len(pet.tasks) == 1
