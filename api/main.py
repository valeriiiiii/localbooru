from database import Database
from mediaScanner import MediaScanner

if __name__ == "__main__":
    config = {
        'db': {'path': '../db/database.json'},
        'content': {
            'image_folder': '../temp'
        }
    }

    media_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mkv', '.webm', '.webp']
    db = Database(config)
    db.load()
    db.sort_by_name()
    db.remove_duplicates()
    scanner = MediaScanner(db, media_extensions)
    scanner.scan_folder(config['content']['image_folder'])
    db.save()
   
    
