class Node:
    def __init__(self, value):
        self.value = value

        self.outbound = []
        self.inbound = []

    def point_to(self, other):
        self.outbound.append(other)
        other.inbound.append(self)

    def __str__(self):
        return f'Node({self.value})'

class Graph:
    def __init__(self, root):
        self._root = root

    def dfs(self):
        vertex = self._root
        visited = []
        stack = [vertex]

        while stack:
            node = stack.pop()

            if node not in visited:
                visited.append(node)

                neighbors = list(node.outbound)
                neighbors.reverse()

                for neighbor in neighbors:
                    stack.append(neighbor)
        return visited

a = Node('a')
b = Node('b')
c = Node('c')
d = Node('d')
a.point_to(b)
b.point_to(c)
c.point_to(d)
d.point_to(a)
b.point_to(d)

g = Graph(a)

print(g.dfs())