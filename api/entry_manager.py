from typing import Dict, List, Optional
from datetime import datetime

class EntryManager:
    def __init__(self, entry: Dict[str, any]):
        self.entry: dict = entry

    def add_tag(self, category: str, tag: str) -> None:
        if category in self.entry["tags"]:
            if tag not in self.entry["tags"][category]:  # Avoid duplicates
                self.tags[category].append(tag)
        else:
            self.tags[category] = [tag]

    def remove_tag(self, category: str, tag: str) -> None:
        if category in self.entry["tags"] and tag in self.entry["tags"][category]:
            self.entry["tags"][category].remove(tag)

    def set_comment(self, comment: str) -> None:
        self.entry["comment"] = comment

    def get_comment(self) -> str:
        return self.entry["comment"]

    def set_creation_date(self, date_str: str) -> None:
        try:
            self.entry["CreationDate"] = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

    def get_creation_date(self) -> Optional[str]:
        return self.entry["CreationDate"].strftime("%Y-%m-%d") if self.entry["CreationDate"] else None

    def set_source(self, source: str) -> None:
        self.entry["Source"] = source

    def get_source(self) -> Optional[str]:
        return self.entry["Source"]

    def __str__(self) -> str:
        return (f"EntryManager(name={self.entry['name']}, filepath={self.entry['filepath']}, "
                f"comment={self.get_comment()}, creation_date={self.get_creation_date()}, "
                f"source={self.get_source()})")
