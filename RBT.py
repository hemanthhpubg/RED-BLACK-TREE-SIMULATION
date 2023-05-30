import pygame
import sys
import time

class Node:
    def __init__(self, val, x, y, level, color):
        self.val = val
        self.left = None    
        self.right = None
        self.parent=None
        self.x = x
        self.y = y
        self.level = level
        self.color = color
        self.null='NO'


class RedBlackTree:
    x = 800
    def __init__(self):
        self.root = None
        self.node_radius = 20
        self.horizontal_spacing = 100
        self.vertical_spacing = 50
        self.screen_width = 800
        self.screen_height = 600
        self.font = pygame.font.SysFont(None, 20)
        self.tree_surface = pygame.Surface((self.screen_width, self.screen_height))
    def insert(self, val):
        new_node = Node(val, 0, 0, 0, 'RED')
        if self.root is None:
            self.root = new_node
            new_node.x = self.screen_width // 2
            new_node.y = self.vertical_spacing
            new_node.level = 0
            new_node.color = 'BLACK'
            return
        curr_node = self.root
        c = 1
        while curr_node:
            if val < curr_node.val:
                if curr_node.left:
                    c += 1
                    curr_node = curr_node.left
                else:
                    curr_node.left = new_node
                    new_node.x = curr_node.x - (self.horizontal_spacing//c)
                    new_node.y = curr_node.y + (self.vertical_spacing)
                    new_node.level = c
                    new_node.parent = curr_node
                    self.fix_insert(new_node)
                    return
            else:
                if curr_node.right:
                    c += 1
                    curr_node = curr_node.right
                else:
                    curr_node.right = new_node
                    new_node.x = curr_node.x + (self.horizontal_spacing//c)
                    new_node.y = curr_node.y + self.vertical_spacing
                    new_node.level = c
                    new_node.parent = curr_node
                    self.fix_insert(new_node)
                    return

    def update_positions(self, node, x, y):
        if node is None:
            return
        if node==self.root:
            x=self.screen_width // 2
            y=self.vertical_spacing
        node.x = x
        node.y = y
        # Recursively update positions of left and right subtree
        self.update_positions(node.left, x - (self.horizontal_spacing // (node.level + 1)), y + self.vertical_spacing)
        self.update_positions(node.right, x + (self.horizontal_spacing // (node.level + 1)), y + self.vertical_spacing)


    def fix_insert(self, new_node):
        while new_node != self.root and new_node.color != 'BLACK' and new_node.parent.color == 'RED':
            if new_node.parent == new_node.parent.parent.left:
                uncle = new_node.parent.parent.right
                if uncle and uncle.color == 'RED':
                    new_node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    new_node.parent.parent.color = 'RED'
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.left_rotate(new_node)
                    new_node.parent.color = 'BLACK'
                    new_node.parent.parent.color = 'RED'
                    self.right_rotate(new_node.parent.parent)
            else:
                uncle = new_node.parent.parent.left
                if uncle and uncle.color == 'RED':
                    new_node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    new_node.parent.parent.color = 'RED'
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.right_rotate(new_node)
                    new_node.parent.color = 'BLACK'
                    new_node.parent.parent.color = 'RED'
                    self.left_rotate(new_node.parent.parent)
        self.root.color = 'BLACK'
        self.update_positions(self.root,self.root.x,self.root.y)
    def left_rotate(self, node):
        y = node.right
        node.right = y.left
        y.parent = node.parent
        y.level=y.level-1
        x=0
        if y.left is not None:
            x=y.left
        if y.right is not None:#y.right->new node that is inserted
            y.right.parent=y
            y.right.level=y.level+1
        if node.parent is None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y
        node.level=y.level+1
        if x!=0:
            x.parent = node
            x.level = node.level + 1

    def inorder_traversal(self,node):
        if node:
            self.inorder_traversal(node.left)
            print(node.val)
            self.inorder_traversal(node.right)
    def right_rotate(self, node):
        y = node.left
        node.left = y.right
        y.parent = node.parent
        y.level=y.level-1
        x=0
        if y.right is not None:
            x=y.right
        if y.left is not None:
            y.left.parent = y
            y.left.level = y.level + 1
        if node.parent is None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.right = node
        node.parent = y
        node.level = node.level + 1
        if x!=0:
            x.parent = node
            x.level = node.level + 1

    def _find_in_order_successor(self, node):
        if node.left is None:
            return node
        else:
            return self._find_in_order_successor(node.left)
    def _find_in_order_predecessor(self, node):
        if node.right is None:
            return node
        else:
            return self._find_in_order_successor(node.right)

    def db(self,node):
            if node==self.root:
                return
            if (node == node.parent.right):
                sibling = node.parent.left
                if (sibling.left is None):
                    sibling.left=Node(0,0,0,0,'BLACK')
                    sibling.left.null='YES'
                if (sibling.right is None):
                    sibling.right=Node(0,0,0,0,'BLACK')
                    sibling.right.null = 'YES'
                if (sibling.color == 'BLACK'):
                    if (sibling.left.color == 'BLACK' and sibling.right.color == 'BLACK'):
                        sibling.color = 'RED'
                        if (node.parent.color == 'RED'):
                            node.parent.color = 'BLACK'
                            return
                        else:
                            self.db(node.parent)
                    elif(sibling.right.color=='RED' and sibling.left.color=='BLACK'):
                        sibling.color = sibling.right.color
                        sibling.right.color='BLACK'
                        self.left_rotate(sibling)
                        self.update_positions(self.root, self.root.x, self.root.y)
                        self.db(node)
                    elif(sibling.left.color=='RED'):
                        sibling.color = sibling.parent.color
                        sibling.parent.color='BLACK'
                        sibling.left.color='BLACK'
                        self.right_rotate(sibling.parent)
                        self.update_positions(self.root, self.root.x, self.root.y)
                        return
                elif(sibling.color=='RED'):
                    sibling.color=sibling.parent.color
                    sibling.parent.color='RED'
                    self.right_rotate(sibling.parent)
                    self.update_positions(self.root, self.root.x, self.root.y)
                    self.db(node)
            elif (node == node.parent.left):
                sibling = node.parent.right
                if (sibling.left is None):
                    sibling.left = Node(0, 0, 0, 0, 'BLACK')
                    sibling.left.null = 'YES'
                if (sibling.right is None):
                    sibling.right = Node(0, 0, 0, 0, 'BLACK')
                    sibling.right.null = 'YES'
                if (sibling.color == 'BLACK'):
                    if (sibling.left.color == 'BLACK' and sibling.right.color == 'BLACK'):
                        sibling.color = 'RED'
                        print("yes")
                        if (node.parent.color == 'RED'):
                            node.parent.color = 'BLACK'
                            return
                        else:
                            self.db(node.parent)
                    elif (sibling.left.color == 'RED' and sibling.right.color == 'BLACK'):
                        sibling.color = sibling.left.color
                        sibling.left = 'BLACK'
                        self.right_rotate(sibling)
                        self.update_positions(self.root, self.root.x, self.root.y)
                        self.db(node)
                    elif (sibling.right.color == 'RED'):
                        sibling.color = sibling.parent.color
                        sibling.parent.color = 'BLACK'
                        sibling.right.color = 'BLACK'
                        self.left_rotate(sibling.parent)
                        self.update_positions(self.root, self.root.x, self.root.y)
                        return
                elif (sibling.color == 'RED'):
                    print("yes")
                    sibling.color = sibling.parent.color
                    sibling.parent.color = 'RED'
                    print(node.val, node.x, node.y)
                    self.left_rotate(sibling.parent)
                    self.update_positions(self.root, self.root.x, self.root.y)
                    print(node.val,node.x,node.y)
                    self.db(node)


    def _delete_node(self, root, node):
        if root is None:
            return root
        if node.val < root.val:
            self._delete_node(root.left, node)
        elif node.val > root.val:
            self._delete_node(root.right, node)
        else:
            if root.left is None and root.right is None:
                if(root.color=='RED'):
                    root.null='YES'
                elif(root.color=='BLACK'):
                    self.db(root)
                    root.null='YES'
                    self.update_positions(self.root, self.root.x, self.root.y)
                    return
            elif root.left is None:
                root.val=root.right.val
                if (root.right.color == 'RED'):
                    root.right.null = 'YES'
                elif (root.right.color == 'BLACK'):
                    self.db(root.right)
                    root.right.null = 'YES'
                    self.update_positions(self.root, self.root.x, self.root.y)
                    return

            elif root.right is None:
                # Node has one child, replace with child
                root.val= root.left.val
                if (root.left.color == 'RED'):
                    root.left.null = 'YES'
                elif (root.left.color == 'BLACK'):
                    self.db(root.left)
                    root.left.null = 'YES'
                    self.update_positions(self.root, self.root.x, self.root.y)
                    return
            else:
                # Node has two children, find in-order successor
                in_order_successor = self._find_in_order_successor(root.right)
                root.val = in_order_successor.val
                self._delete_node(root.right, in_order_successor)

    def find_node(self, value):
        node = self.root
        while node is not None:
            if value < node.val:
                node = node.left
            elif value > node.val:
                node = node.right
            else:
                return node
        return None

    def draw_tree(self, node, x_offset=0, y_offset=0):
        if node:
            if(node.null == 'NO'):
                x = node.x
                y = node.y
                text_surface = self.font.render(str(x), True, pygame.Color('black'))
                text_rect = text_surface.get_rect(center=(x+50, y))
                self.tree_surface.blit(text_surface, text_rect)
                pygame.draw.circle(self.tree_surface, pygame.Color(node.color), (x, y), self.node_radius)
                text_surface = self.font.render(str(node.val), True, pygame.Color('white'))
                text_rect = text_surface.get_rect(center=(x, y))
                self.tree_surface.blit(text_surface, text_rect)
            if node.left :
                if node.left.null=='NO':
                    left_x_offset = -50  # change this value to adjust the horizontal spacing between nodes
                    left_y_offset = 50  # change this value to adjust the vertical spacing between nodes
                    pygame.draw.line(self.tree_surface, pygame.Color('black'), (x, y + self.node_radius),(node.left.x, node.left.y - self.node_radius), 2)
                    self.draw_tree(node.left, left_x_offset, left_y_offset)
            if node.right:
                if node.right.null=='NO':
                    right_x_offset = 50  # change this value to adjust the horizontal spacing between nodes
                    right_y_offset = 50  # change this value to adjust the vertical spacing between nodes
                    pygame.draw.line(self.tree_surface, pygame.Color('black'), (x, y + self.node_radius),(node.right.x, node.right.y - self.node_radius), 2)
                    self.draw_tree(node.right, right_x_offset, right_y_offset)
    def display_tree(self, screen):
        self.tree_surface.fill(pygame.Color('white'))
        self.draw_tree(self.root,0,0)
        screen.blit(self.tree_surface, (0, 0))

class InputBox:
    def __init__(self, x, y, width, height,color, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color(color)
        self.text = text
        self.font = pygame.font.SysFont(None, 20)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        text_surface = self.font.render(self.text, True, pygame.Color(self.color))
        text_rect = text_surface.get_rect(center=self.rect.center)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(text_surface, text_rect)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Binary Tree Visualization")
    clock = pygame.time.Clock()

    # Create a binary tree and an input box for user input
    tree = RedBlackTree()
    input_box = InputBox(80, 550, 200, 30,'blue')
    input_box2 = InputBox(450, 550, 200, 30,'red')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            input_box.handle_event(event)
            input_box2.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        val = int(input_box.text)
                        tree.insert(val)
                        input_box.text = ''
                    except ValueError:
                        print("Invalid input!")
                elif event.key == pygame.K_RSHIFT:
                    try:
                        val2 = int(input_box2.text)
                        n=tree.find_node(val2)
                        tree._delete_node(tree.root,n)
                        input_box2.text = ''
                    except ValueError:
                        print("Invalid input!")
        screen.fill(pygame.Color('white'))
        tree.display_tree(screen)
        pygame.draw.rect(screen, input_box.color, input_box.rect, 2)
        pygame.draw.rect(screen, input_box2.color, input_box2.rect, 2)
        text_surface = input_box.font.render(input_box.text, True, pygame.Color('black'))
        text_surface2 = input_box2.font.render(input_box2.text, True, pygame.Color('black'))
        screen.blit(text_surface, (input_box.rect.x + 5, input_box.rect.y + 5))
        screen.blit(text_surface2, (input_box2.rect.x + 5, input_box2.rect.y + 5))
        font = pygame.font.Font(None, 20)
        text_surface = font.render("INSERT", True, "black")
        screen.blit(text_surface, (10, 557))
        font = pygame.font.Font(None, 20)
        text_surface = font.render("DELETE", True, "black")
        screen.blit(text_surface, (380, 557))
        pygame.display.update()
        clock.tick(60)
width=800
height=600