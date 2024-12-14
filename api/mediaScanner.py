import os
from typing import List, Dict, Any
from database import Database
from fileRename import rename_file_to_md5 as renameFile

def create_entry_template(name: str, filepath: str) -> Dict[str, Any]:
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
                "General": [],
                "Meta" : [],
                "Authors": []
            },
            "comment": f"This is a media file named {name}.",
            "CreationDate": "",
            "Source": ""
        }


class MediaScanner:
    def __init__(self, db: Database, media_extensions: List[str]):
        """Initialize the media scanner with a database and media file extensions."""
        self.db = db
        self.media_extensions = media_extensions

    def scan_folder(self, folder_path: str) -> None:
        """Scan the specified folder recursively for media files."""
        for root, dirs, files in os.walk(folder_path):
            # Ignore the '.thumb' directory and its subdirectories
            if '.thumb' in dirs:
                dirs.remove('.thumb')  # This will prevent os.walk from going into the .thumb directory

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
            new_file_path = renameFile(file_path)
            new_file_name = os.path.basename(new_file_path)
            entry = create_entry_template(new_file_name, new_file_path)
            self.db.append(entry)

    
