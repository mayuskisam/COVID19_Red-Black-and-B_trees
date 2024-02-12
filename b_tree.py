class bNode(object):
    def __init__(self, isLeaf=False):
        self.isLeaf = isLeaf
        self.keys = []
        self.children = []


class bTree(object):
    def __init__(self, n):
        self.root = bNode(True)
        self.n = n

    # adjusted code from https://gist.github.com/natekupp/1763661
    def insert(self, key):
        r = self.root
        if len(r.keys) == (2 * self.n) - 1:
            s = bNode()
            self.root = s
            s.children.insert(0, r)
            self.split(s, 0)
            self.nonfull(s, key)
        else:
            self.nonfull(r, key)

    # decide whether to insert a key or a child
    def nonfull(self, node, key):
        i = len(node.keys) - 1
        if node.isLeaf:
            node.keys.append(0)
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                i -= 1
            node.keys[i+1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            if len(node.children) - 1 <= i:
                i = len(node.children) - 1
            else:
                i += 1
            if len(node.children[i].keys) == (2 * self.n) - 1:
                self.split(node, i)
                if key > node.keys[i]:
                    i += 1
            self.nonfull(node.children[i], key)

    # split the children if necessary
    def split(self, node, i):
        num = self.n
        y = node.children[i]
        z = bNode(isLeaf=y.isLeaf)

        node.children.insert(i+1, z)
        node.keys.insert(i, y.keys[num - 1])

        z.keys = y.keys[num:(2 * num) - 1]
        y.keys = y.keys[0:num - 1]

        if not y.isLeaf:
            z.children = y.children[num:(2 * num)]
            y.children = y.children[0:num]

    def search(self, root, country, date):  # search given country and date
        # traverse through the tree, checking if the country and date match the key
        stack = []  # stack of node, index pairs
        stack.append((root, 0))
        while len(stack) > 0:
            [node, i] = stack.pop()
            if not node.children:  # no children
                for key in node.keys:
                    if key[1][0] == country and key[1][1] == date:
                        return key[0]
            elif i < len(node.children):
                if i > 0:
                    if node.keys[i - 1][1][0] == country and node.keys[i - 1][1][1] == date:
                        return node.keys[i - 1][0]
                stack.append((node, i + 1))
                stack.append((node.children[i], 0))

    def getCountries(self, root):  # returns a list of all countries in the tree
        # traverse through the tree, adding the country to the list if it is not already in the list
        countries = []
        stack = []  # stack of node, index pairs
        stack.append(root)
        while len(stack) > 0:
            node = stack.pop()
            if node.children:
                for child in node.children:
                    stack.append(child)
            for key in node.keys:
                if key[1][0] not in countries:
                    countries.append(key[1][0])
        return countries

    def preOrder(self, root):
        print("Preorder traversal: ")
        # iterative
        stack = []
        stack.append(root)
        while len(stack) > 0:
            node = stack.pop()
            for key in node.keys:
                print(key)
            if node.children:
                # reverse the order of the children so right is visited first
                for child in reversed(node.children):
                    stack.append(child)

    # adjusted code from https://stackoverflow.com/questions/63872883/how-to-traverse-btree-in-order-without-recursion-in-iterative-style
    def inOrder(self, root):
        print("Inorder traversal: ")
        # iterative
        stack = []  # stack of node, index pairs
        stack.append((root, 0))
        while len(stack) > 0:
            [node, i] = stack.pop()
            if not node.children:  # no children
                for key in node.keys:
                    print(key)
            elif i < len(node.children):
                if i > 0:
                    print(node.keys[i - 1])
                stack.append((node, i + 1))
                stack.append((node.children[i], 0))

    def postOrder(self, root):
        print("Postorder traversal: ")
        # iterative
        stack = []
        stack.append(root)
        while len(stack) > 0:
            node = stack.pop()
            if node.children:
                for child in node.children:
                    stack.append(child)
            for key in node.keys:
                print(key)
