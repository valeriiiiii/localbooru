## LocalBooru 

Local booru like media tagging tool(?)

Simple adaptive web app for PCs, tablets and phones.

## Graph view for dev

```
+----------------+                               +-------------------+
|      GUI       |                               | Core Components:  |
+----------------+                               |                   |
        ^                                        | - Find            |
        |                                        |   - Simple        |
        v                                        |   - Advanced      |
+----------------+       +----------------+      | - Tag Management  |
|      CLI       |<----->|      API       |<---->|   - Suggest tags  |
+----------------+       +----------------+      |   - Add/Delete    |
        ^                        ^               | - Thumbnail Gen.  |
        |                        |               |   - Daemon        |
        |                        v               |   - PIL           |
        v              +----------------+        |   - Sizes:        |
+----------------+     |    DATABASE    |        |     - Small       |
|      Back      |     |     (JSON)     |        |     - Medium      |
+----------------+     +----------------+        |     - XL          |
                                                 +-------------------+

JSON Output:
- path
- sth_path (small thumbnail path)
- mth_path (medium thumbnail path)
- lth_path (large thumbnail path)
- tags
- comments
- authors
- meta
```

## TODO list

- [ ] For thumbler add black/white lists to include/exclude filetypes which will be thumbled
- [x] Make thumbler as class
- [ ] Web interface (look at gelbooru/rule34 as an example)

## TODO list from jsonDB.py:

- [x] **Spit classes in different files**

- [x] tag mangement (add tag to an existing entry) and etc
- [ ] all entried will be existing cause a scanner will add them if not. Also uploading a picture would cause db to add entry to it and 
- [x] renamer module changing the name of the pic to it's hash 
- [x] if file does not exist then remove it's entry (check consistency?)
