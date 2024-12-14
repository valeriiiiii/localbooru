from database import Database
from mediaScanner import MediaScanner
from tagManager import TagManager
from thumbManager import ThumbManager
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
    #untagged = db.get_untagged_entries()
    #entry = db.get("7671139c4be1566b249c01d41489fe4b.jpg")
    #for i in db:
    #    thumb_m=ThumbManager(i)
    #    thumb_m.check_and_generate_thumbnails()
    #    print(i)
    #tm = TagManager(entry)
    #tm.remove_tag("MyCategory",["test1","test2","test3"])
    #thumb_m=ThumbManager(entry)
    #thumb_m.check_and_generate_thumbnails()
 
