import sys

def analyze_tree_structure(root_node) -> dict:
    """
    Analyzes binary tree data structures to measure node count, height, 
    leaf density, and memory overhead.
    """
    if not root_node or hasattr(root_node, 'key') and root_node.key == 0 and not hasattr(root_node, 'value'):
        # Empty or NIL node check
        return {
            "total_nodes": 0,
            "max_height": 0,
            "leaf_count": 0,
            "is_balanced": True
        }

    total_nodes = 0
    leaf_count = 0
    max_height = 0

    # BFS / DFS traversal
    def traverse(node, current_height):
        nonlocal total_nodes, leaf_count, max_height
        if not node or (hasattr(node, 'color') and hasattr(node, 'key') and node.key == 0 and node.left is None):
            return

        total_nodes += 1
        max_height = max(max_height, current_height)

        left_child = getattr(node, 'left', None)
        right_child = getattr(node, 'right', None)

        is_left_nil = left_child is None or (hasattr(left_child, 'key') and left_child.key == 0 and left_child.left is None)
        is_right_nil = right_child is None or (hasattr(right_child, 'key') and right_child.key == 0 and right_child.left is None)

        if is_left_nil and is_right_nil:
            leaf_count += 1

        if not is_left_nil:
            traverse(left_child, current_height + 1)
        if not is_right_nil:
            traverse(right_child, current_height + 1)

    traverse(root_node, 1)

    return {
        "total_nodes": total_nodes,
        "max_height": max_height,
        "leaf_count": leaf_count,
        "is_balanced": max_height <= (total_nodes.bit_length() + 2) if total_nodes > 0 else True
    }
