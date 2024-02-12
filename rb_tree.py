class rbNode:
    def __init__(self, parent, country, cases, date):
        self.country = country
        self.cases = cases
        self.date = date
        self.left = None
        self.right = None
        self.parent = parent
        self.isRed = True
        self.blackHeight = 0


class rbTree:
    def __init__(self):
        self.root = None
        self.nodeCount = 0
        self.n = rbNode(None, None, None, None)
        self.n.color = False
        self.n.left = None
        self.n.right = None
        self.n.root = self.n

    # code for insert based on lecture slides and https://favtutor.com/blogs/red-black-tree-python guidelines
    def insert(self, root, name, casesNum, dateVal):
        leftChild = False
        node = rbNode(None, name, casesNum, dateVal)  # creating the new node
        parent = None
        while root is not None:  # iterating down the tree using BST tactics
            parent = root
            if casesNum <= root.cases:
                root = root.left
                leftChild = True
            else:
                root = root.right
                leftChild = False
        self.nodeCount += 1

        if self.nodeCount == 1:  # the new node is the root, so it has to be black
            node.isRed = False
            self.root = node

        # assigning the appropriate left or right value
        if parent is not None and leftChild and self.nodeCount > 1:
            parent.left = node
        elif parent is not None and self.nodeCount > 1:
            parent.right = node

        node.parent = parent
        if self.nodeCount >= 3 and node.parent is not None and node.parent.parent is not None:  # checking for a grandparent node
            self.checkConditions(node)

    def leftRotation(self, node):  # for right right case
        temp = node.right.left
        tempParent = node.right
        node.right.left = node
        node.isRed = not node.isRed
        if node.parent is None:
            node.right.parent = None
            self.root = node.right
            self.root.isRed = False
        elif node == node.parent.left:
            node.parent.left = node.right
            node.right.isRed = not node.right.isRed
        else:
            node.parent.right = node.right
            node.right.isRed = not node.right.isRed
        node.right = temp
        node.parent = tempParent

    def rightRotation(self, node):  # for left left case
        temp = node.left.right
        tempParent = node.left
        node.left.right = node
        node.isRed = not node.isRed
        if node.parent is None:
            node.left.parent = None
            self.root = node.left
            self.root.isRed = False
        elif node == node.parent.right:
            node.parent.right = node.left
            node.left.isRed = not node.left.isRed
        else:
            node.parent.left = node.left
            node.left.isRed = not node.left.isRed
        node.left = temp
        node.parent = tempParent

    def checkConditions(self, node):
        while node is not None and node.isRed and node.parent is not None and node.parent.isRed:
            grandparent = node.parent.parent
            if grandparent.left == node.parent:  # parent is left child of grandparent
                uncle = grandparent.right
                if uncle is None or uncle.isRed == False:  # the uncle is a black node, rotation required
                    if node == node.parent.left:  # left left case
                        self.rightRotation(grandparent)
                    else:  # left right case
                        self.leftRotation(node.parent)
                        node.parent = grandparent
                        self.rightRotation(grandparent)
                        node.parent = grandparent
                        node.left.isRed = True
                        node.right.isRed = True
                        node.isRed = False
                else:  # uncle is red, flip colors
                    node.parent.isRed = not node.parent.isRed  # flipping the color of the parent
                    if grandparent != self.root:
                        grandparent.isRed = not grandparent.isRed
                    if uncle is not None:
                        uncle.isRed = not uncle.isRed

            else:  # parent is right child of grandparent
                uncle = grandparent.left
                if uncle is None or uncle.isRed == False:  # the uncle is a black node, rotation required
                    if node == node.parent.right:  # right right case
                        self.leftRotation(grandparent)
                    else:  # right left case
                        self.rightRotation(node.parent)
                        node.parent = grandparent
                        self.leftRotation(grandparent)
                        node.parent = grandparent
                        node.left.isRed = True
                        node.right.isRed = True
                        node.isRed = False
                else:  # uncle is red, flip colors
                    node.parent.isRed = not node.parent.isRed  # flipping the color of the parent
                    if grandparent != self.root:
                        grandparent.isRed = not grandparent.isRed
                    if uncle is not None:
                        uncle.isRed = not uncle.isRed
            node = node.parent

    def search(self, root, country, date):  # return cases for a given country and date
        stack = []
        while True:
            if root is not None:
                stack.append(root)
                root = root.left
            elif stack:
                root = stack.pop()
                if root.country == country and root.date == date:
                    return root.cases
                root = root.right
            else:
                break
        return None

    def getCountries(self, root):  # returns a list of all countries in the tree
        countries = []
        stack = []
        while True:
            if root is not None:
                stack.append(root)
                root = root.left
            elif stack:
                root = stack.pop()
                # make sure we don't add duplicates
                if root.country not in countries:
                    countries.append(root.country)
                root = root.right
            else:
                break
        return countries

    # adjusted code from https://www.programiz.com/dsa/red-black-tree for deletion section
    # transplant the red-black tree when we find the desired node to delete
    def transplant(self, node1, node2):
        if node1.parent is None:
            self.n.root = node2
        elif node1 == node1.parent.left:
            node1.parent.left = node2
        else:
            node1 = node2

        node2.parent = node1.parent

    # find the smallest value of a tree
    def min(self, node):
        while node.left != self.n:
            node = node.left
        return node

    # balance the red-black tree after deletion
    def balanceD(self, node):
        while node != self.n.root and node.isRed == False:
            # left child case
            if node == node.parent.left:
                r = node.parent.right
                if r.isRed == True:
                    r.isRed = False
                    node.parent.isRed = True
                    self.leftRotation(node.parent)
                    r = node.parent.right

                # all black children nodes case
                if r.left.isRed == False and r.right.isRed == False:
                    r.isRed = 1
                    node = node.parent
                # other cases
                else:
                    if r.right.isRed == False:
                        r.left.isRed = 0
                        r.isRed = 1
                        self.rightRotation(r)
                        r = node.parent.right

                    r.isRed = node.parent.isRed
                    node.parent.isRed = False
                    r.right.isRed = False
                    self.leftRotation(node.parent)
                    node = self.n.root

            # right child case
            else:
                r = node.parent.left
                if r.isRed == True:
                    r.isRed = False
                    node.parent.isRed = True
                    self.rightRotation(node.parent)
                    r = node.parent.left

                if r.right.isRed == False and r.left.isRed == False:
                    r.isRed = 1
                    node = node.parent
                else:
                    if r.left.isRed == False:
                        r.right.isRed = False
                        r.isRed = True
                        self.leftRotation(r)
                        r = node.parent.left

                    r.isRed = node.parent.isRed
                    node.parent.isRed = False
                    r.left.isRed = False
                    self.rightRotation(node.parent)
                    node = self.n.root

        node.isRed = False

    def preOrder(self, root):
        # iterative pre-order traversal
        print("Pre-order traversal: ")
        stack = []
        stack.append(root)
        while stack:
            node = stack.pop()
            print(node.country, node.date, node.cases)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

    def inOrder(self, root):
        # iterative in-order traversal
        print("In-order traversal")
        stack = []
        while True:
            if root is not None:
                stack.append(root)
                root = root.left
            elif stack:
                root = stack.pop()
                print(root.country, root.date, root.cases)
                root = root.right
            else:
                break

    # peek at the top of the stack
    # adapted from https://www.geeksforgeeks.org/iterative-postorder-traversal-using-stack/
    def peek(self, stack):
        if len(stack) > 0:
            return stack[-1]
        return None

    # adapted from https://www.geeksforgeeks.org/iterative-postorder-traversal-using-stack/
    def postOrder(self, root):
        # iterative post-order traversal
        print("Post-order traversal: ")
        stack = []
        while True:
            while root:
                if root.right:
                    stack.append(root.right)
                stack.append(root)
                root = root.left
            root = stack.pop()
            if root.right != None and self.peek(stack) == root.right:
                stack.pop()
                stack.append(root)
                root = root.right
            else:
                print(root.country, root.date, root.cases)
                root = None
            if len(stack) <= 0:
                break
