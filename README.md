да## LocalBooru 

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
```
