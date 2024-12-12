import json
from typing import Dict, Any, List
import os

class Database:
    def __init__(self, config: Dict[str, Any]):
        """Initialize the database with the given configuration."""
        self.db_path = config['db']['path']
        self.db = {}

    def load(self) -> None:
        """Load data from a JSON file into the database."""
        try:
            with open(self.db_path, 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {}
        except json.JSONDecodeError:
            print("Error decoding JSON from the file.")
            self.db = {}

    def save(self) -> None:
        """Save the current database to a JSON file."""
        with open(self.db_path, 'w') as f:
            json.dump(self.db, f, indent=4)
    def append(self, item: Dict[str, Any], update_if_exists: bool = False) -> None:
        """Add a new entry to the database, handling duplicates."""
        if "name" not in item:
            print("Item must have a 'name' key.")
            return
        if item["name"] in self.db:
            if update_if_exists:
                self.db[item["name"]].update(item)
                print(f"Updated entry: {item['name']}")
            else:
                print(f"Duplicate entry found for '{item['name']}'. Entry not added.")
                return -1

        self.db[item["name"]] = item
        print(f"Added entry: {item['name']}")
        return 0

    def remove(self, item: Dict[str, Any]) -> None:
        """Remove an item from the database."""
        self.db.pop(item["name"], None)  # Avoid KeyError

    def pop(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Remove and return an item from the database."""
        return self.db.pop(item["name"], None)  # Avoid KeyError

    def find(self, query: Dict[str, Any], ignore_case: bool = True) -> List[Dict[str, Any]]:
        """Find items in the database based on the query."""
        results = []
        for item in self.db.values():
            item_tags = {key: [tag.lower() for tag in tags] for key, tags in item["tags"].items()} if ignore_case else item["tags"]
            query_include_tags = {key: [tag.lower() for tag in tags] for key, tags in query.get("include_tags", {}).items()} if ignore_case else query.get("include_tags", {})
            query_exclude_tags = {key: [tag.lower() for tag in tags] for key, tags in query.get("exclude_tags", {}).items()} if ignore_case else query.get("exclude_tags", {})

            if all(tag in item_tags.get(key, []) for key, tags in query_include_tags.items() for tag in tags) and \
               all(tag not in item_tags.get(key, []) for key, tags in query_exclude_tags.items() for tag in tags):
                results.append(item)
        return results
    
    def sort_by_name(self) -> None:
        """Sort the database entries by the name of the entry and update the file."""
        # Sort the database entries by name
        sorted_db = dict(sorted(self.db.items(), key=lambda item: item[1]["name"]))
        self.db = sorted_db  # Update the database with sorted entries
        print(sorted_db.keys())
        print("Database sorted by name and updated in the file.")

    def entry_exists(self, name: str) -> bool:
        """Check if an entry with the given name already exists in the database."""
        return name in self.db

    def remove_duplicates(self) -> None:
        """Remove duplicate entries from the database based on the entry name."""
        unique_entries = {}
        for item in self.db.values():
            unique_entries[item["name"]] = item  # This will overwrite duplicates

        self.db = unique_entries  # Update the database with unique entries
        self.save()  # Save the updated database to the file
        print("Duplicates removed. Database updated with unique entries.")
        
class MediaScanner:
    def __init__(self, db: Database, media_extensions: List[str]):
        """Initialize the media scanner with a database and media file extensions."""
        self.db = db
        self.media_extensions = media_extensions

    def scan_folder(self, folder_path: str) -> None:
        """Scan the specified folder recursively for media files."""
        for root, _, files in os.walk(folder_path):
            for file in files:
                if self.is_media_file(file):
                    self.process_file(os.path.join(root, file))

    def is_media_file(self, filename: str) -> bool:
        """Check if the file is a media file based on its extension."""
        return any(filename.lower().endswith(ext) for ext in self.media_extensions)

    def process_file(self, file_path: str) -> None:
        """Process the media file and create an entry in the database."""
        file_name = os.path.basename(file_path)
        if file_name not in self.db.db:
            entry = self.create_entry_template(file_name, file_path)
            self.db.append(entry)
            
    def create_entry_template(self, name: str, filepath: str) -> Dict[str, Any]:
        """Create a template entry for the media file."""
        return {
            "name": name,
            "filepath": filepath,
            "thumbnail": {
                "small": "",
                "medium": "",
                "large": ""
            },
            "tags": {
                "Style": [],
                "Authors": []
            },
            "comment": f"This is a media file named {name}.",
            "CreationDate": "",  # Optional
            "Source": ""  # Optional
        }

# Example usage
if __name__ == "__main__":
    config = {
        'db': {'path': '../db/database.json'},
        'content' : {
        'image_folder' : '../temp'
            }
    }
    
    media_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mkv', '.webm', '.webp']  # Add more as needed
    db = Database(config)
    db.load()
    db.sort_by_name()
    db.remove_duplicates()
    scanner = MediaScanner(db, media_extensions)
    
    # Specify the folder to scan

    scanner.scan_folder(config['content']['image_folder'])

    # Save the database after scanning
    db.save()

