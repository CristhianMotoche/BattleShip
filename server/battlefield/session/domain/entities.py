from dataclasses import dataclass


@dataclass
class Session:
    id: int
    key: str

    def to_dict(self):
        return {"id": self.id, "key": self.key}
