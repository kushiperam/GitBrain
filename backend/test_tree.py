import json

from app.services.tree_builder import build_directory_tree


tree = build_directory_tree(
    "repositories/Hello-World.git"
)


print(
    json.dumps(
        tree,
        indent=4
    )
)