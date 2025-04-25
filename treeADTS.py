from collections import Counter
from dataStructure import countChars, treeBuilder, assignCode, buildCodeString

with open('test2.txt', 'r') as file:
    text = file.read()

freqs = countChars(text)
tree = treeBuilder(freqs)
codes = assignCode(tree)
encoded_text = buildCodeString(codes, text)

def make_node(value):
    return [value, []]

def add_node(tree, parent_value, new_value):
    if tree is None:
        return make_node(new_value)
    
    if tree[0] == parent_value:
        tree[1].append(make_node(new_value))
        return tree
    
    for child in tree[1]:
        result = add_node(child, parent_value, new_value)
        if result:
            return tree
    return tree

def delete_node(tree, value_to_delete):
    if tree is None:
        return None
    
    new_children = []
    for child in tree[1]:
        if child[0] == value_to_delete:
            continue
        else:
            new_children.append(delete_node(child, value_to_delete))
    tree[1] = [c for c in new_children if c is not None]

    if tree[0] == value_to_delete:
        return None
    return tree

def display_tree(tree, prefix="", is_last=True):
    if tree is None:
        return
    
    connector = "└── " if is_last else "├── "
    print(prefix + connector + str(tree[0]))

    child_count = len(tree[1])
    for i, child in enumerate(tree[1]):
        is_last_child = (i == child_count - 1)
        new_prefix = prefix + ("    " if is_last else "│   ")
        display_tree(child, new_prefix, is_last_child)


def tree_height(tree):
    if tree is None:
        return 0
    if not tree[1]:
        return 1
    return 1 + max(tree_height(child) for child in tree[1])

# Start with a root node
print("🔧 Creating root node 'A'")
tree = make_node("A")

print("\n➕ Adding nodes:")
add_node(tree, "A", "B")   # B is a child of A
print("Added 'B' under 'A'")
add_node(tree, "A", "C")   # C is a child of A
print("Added 'C' under 'A'")
add_node(tree, "B", "D")   # D is a child of B
print("Added 'D' under 'B'")
add_node(tree, "B", "E")   # E is a child of B
print("Added 'E' under 'B'")
add_node(tree, "C", "F")   # F is a child of C
print("Added 'F' under 'C'")

# Display the full tree
print("\n🌳 Tree Structure:")
display_tree(tree)

# Get and show height
print("\n📏 Tree Height:")
print("Height:", tree_height(tree))

# Delete a node and show updated tree
print("\n❌ Deleting node 'B' and its children (D and E)...")
delete_node(tree, "B")

print("\n🌳 Tree Structure After Deletion:")
display_tree(tree)

# New height after deletion
print("\n📏 Tree Height After Deletion:")
print("Height:", tree_height(tree))
print(tree)


