import fnmatch

# Function to search by single or multiple tags with exclusions and wildcards
def search_by_tags(data, search_tags):
    """
    Searches the media data for items that match all the specified tags,
    exclude tags with a minus sign, and supports wildcard matching with asterisks.

    :param data: Dictionary containing media information.
    :param search_tags: List of tags to search for, including exclusions (-tag) and wildcards (*pattern*).
    :return: List of items matching the tags.
    """
    results = []

    # Separate positive, negative, and wildcard tags
    positive_tags = [tag for tag in search_tags if not tag.startswith("-") and "*" not in tag]
    exclude_tags = [tag[1:] for tag in search_tags if tag.startswith("-")]
    wildcard_tags = [tag for tag in search_tags if "*" in tag]

    for key, value in data.items():
        tags = value.get("tags", {})
        # Flatten all tags into a single list
        all_tags = [tag for category_tags in tags.values() for tag in category_tags]

        # Check for positive tags (all must match)
        if not all(tag in all_tags for tag in positive_tags):
            continue

        # Check for excluded tags (none must match)
        if any(tag in all_tags for tag in exclude_tags):
            continue

        # Check for wildcard tags (at least one must match each pattern)
        if not all(any(fnmatch.fnmatch(tag, pattern) for tag in all_tags) for pattern in wildcard_tags):
            continue

        # If all checks pass, add to results
        results.append(value)

    return results
