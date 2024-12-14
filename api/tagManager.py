#this is a template for tag manager
class TagManager:
    def __init__(self, tags: Dict[str, List[str]]):
        """Initialize the TagManager with a dictionary of tags."""
        self.tags = tags

    def add_tag(self, category: str, tag: str) -> None:
        """Add a tag to a specific category."""
        if category not in self.tags:
            self.tags[category] = []
        if tag not in self.tags[category]:
            self.tags[category].append(tag)
            print(f"Added tag '{tag}' to category '{category}'.")
        else:
            print(f"Tag '{tag}' already exists in category '{category}'.")

    def remove_tag(self, category: str, tag: str) -> None:
        """Remove a tag from a specific category."""
        if category in self.tags and tag in self.tags[category]:
            self.tags[category].remove(tag)
            print(f"Removed tag '{tag}' from category '{category}'.")
        else:
            print(f"Tag '{tag}' not found in category '{category}'.")

    def get_tags(self, category: str) -> List[str]:
        """Get all tags in a specific category."""
        return self.tags.get(category, [])

    def clear_tags(self, category: str) -> None:
        """Clear all tags in a specific category."""
        if category in self.tags:
            self.tags[category] = []
            print(f"Cleared all tags in category '{category}'.")
        else:
            print(f"Category '{category}' not found.")

    def __repr__(self) -> str:
        """Return a string representation of the tags."""
        return f"TagManager(tags={self.tags})"
        
