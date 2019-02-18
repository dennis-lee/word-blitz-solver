class Trie:
    def __init__(self, target):
        with open(target) as f:
            self.root = Node(None)

            for line in f:
                word = line.strip().lower()
                self.root.insert(word, self.root)


class Node:
    def __init__(self, value):
        self.value = value
        self.children = {}
        self.acceptable = False

    def __repr__(self):
        return self.value if self.value else 'root'

    def get_child(self, value):
        return self.children.get(value)

    def insert(self, current_string, node):
        head = current_string[0]

        if head in node.children:
            next_node = node.get_child(head)

        else:
            next_node = Node(head)
            node.children[head] = next_node

        if len(current_string) > 1:
            return self.insert(current_string[1:], next_node)

        else:
            next_node.acceptable = True
