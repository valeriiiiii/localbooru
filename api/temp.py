#this is temp file for snippet testing
from typing import Dict, Any, List
from mediaScanner import create_entry_template

def get_untagged_categories(entry: Dict[str, Any]) -> List[str]:
    """Return a list of tag categories that are untagged."""
    tags = entry.get("tags", {})
    untagged_categories = []

    # Iterate over the tags dictionary
    for category, tag_list in tags.items():
        if not tag_list:  # Check if the list is empty
            untagged_categories.append(category)

    return untagged_categories

# Example usage
entry = create_entry_template("example_image.jpg", "/path/to/example_image.jpg")
entry["tags"]["General"] = []  # No general tags
entry["tags"]["Meta"] = ["Resolution: 1920x1080"]  # Meta tag present
entry["tags"]["Authors"] = []  # No authors

untagged = get_untagged_categories(entry)
print("Untagged categories:", untagged)

