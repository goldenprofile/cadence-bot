from dataclasses import dataclass


@dataclass(frozen=True)
class Reminder:
    id: int
    title: str
    schedule: str
    chat_id: int
    enabled: bool
    created_at: str
