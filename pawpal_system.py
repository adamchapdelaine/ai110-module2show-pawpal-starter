from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    category: str
    duration: int
    priority: str

    def add_task(self) -> None:
        pass

    def edit_task(self) -> None:
        pass

    def remove_task(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    info: str
    tasks: List[Task] = field(default_factory=list)


@dataclass
class Owner:
    name: str
    info: str
    pets: List[Pet] = field(default_factory=list)


@dataclass
class Scheduler:
    owner: Owner
    scheduled_tasks: List[Task] = field(default_factory=list)

    def schedule_task(self) -> None:
        pass

    def get_todays_tasks(self) -> List[Task]:
        pass
