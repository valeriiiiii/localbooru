#this is a template for tag manager
from typing import Dict, Any, List

class TagManager:
    def __init__(self, tags: Dict[str, List[str]]):
        """Initialize the TagManager with a dictionary of tags."""
        self.tags = tags

    def add_tag(self, category: str, tags) -> None:
        """Add one or more tags to a specific category."""
        if category not in self.tags:
            self.tags[category] = []
        
        # Ensure tags is a list
        if isinstance(tags, str):
            tags = [tags]  # Convert single tag string to a list
        
        for tag in tags:
            if tag not in self.tags[category]:
                self.tags[category].append(tag)
                print(f"Added tag '{tag}' to category '{category}'.")
            else:
                print(f"Tag '{tag}' already exists in category '{category}'.")

    def remove_tag(self, category: str, tags) -> None:
        """Remove one or more tags from a specific category."""
        if category in self.tags:
            # Ensure tags is a list
            if isinstance(tags, str):
                tags = [tags]  # Convert single tag string to a list
            
            for tag in tags:
                if tag in self.tags[category]:
                    self.tags[category].remove(tag)
                    print(f"Removed tag '{tag}' from category '{category}'.")

                    # Check if the category is empty and not one of the protected categories
                    if not self.tags[category] and category not in ["General", "Meta", "Author"]:
                        del self.tags[category]
                        print(f"Removed empty category '{category}'.")
                else:
                    print(f"Tag '{tag}' not found in category '{category}'.")
        else:
            print(f"Category '{category}' does not exist.")

    def get_tags(self, category: str) -> List[str]:
        """Get all tags in a specific category."""
        return self.tags.get(category, [])

    def clear_tags(self, category: str) -> None:
        """Clear all tags in a specific category."""
        if category in self.tags:
            self.tags[category] = []
            print(f"Cleared all tags in category '{category}'.")
            if not self.tags[category] and category not in ["General", "Meta", "Author"]:
                        del self.tags[category]
                        print(f"Removed empty category '{category}'.")
        else:
            print(f"Category '{category}' not found.")
    
    def get_untagged_categories(self) -> List[str]:
        """Return a list of tag categories that are untagged."""
        tags = self.tags
        untagged_categories = []
        # Iterate over the tags dictionary
        for category, tag_list in tags.items():
            if not tag_list:  # Check if the list is empty
                untagged_categories.append(category)

        return untagged_categories

    def __repr__(self) -> str:
        """Return a string representation of the tags."""
        return f"TagManager(tags={self.tags})"
