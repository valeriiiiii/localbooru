import os
from typing import List, Dict, Any
from database import Database


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
            "CreationDate": "",
            "Source": ""
        }