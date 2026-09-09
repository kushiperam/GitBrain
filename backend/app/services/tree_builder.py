import os


IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    ".idea",
    ".vscode",
}


def build_directory_tree(path: str):
    """
    Build repository directory tree.
    """

    name = os.path.basename(path)

    tree = {
        "name": name,
        "type": "folder",
        "children": []
    }


    try:

        items = os.listdir(path)

    except PermissionError:

        return tree


    for item in sorted(items):

        item_path = os.path.join(
            path,
            item
        )


        if os.path.isdir(item_path):

            if item in IGNORE_DIRS:
                continue


            tree["children"].append(
                build_directory_tree(item_path)
            )


        else:

            tree["children"].append(
                {
                    "name": item,
                    "type": "file"
                }
            )


    return tree