from database import Database
from mediaScanner import MediaScanner
from tagManager import TagManager

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
    #db.sort_by_name()
    #db.remove_duplicates()
    #scanner = MediaScanner(db, media_extensions)
    #scanner.scan_folder(config['content']['image_folder'])
    #db.save()
    untagged = db.get_untagged_entries()
    entry = db.get("d5dae5a6db84ea2fd8a843bafdea7bf0.jpg")
    tm = TagManager(entry["tags"])
    #tm.remove_tag("MyCategory",["test1","test2","test3"])
    print(untagged[0][2])
    db.save()
