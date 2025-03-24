import numpy as np
from manim import *


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class PrefixTree:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        current = self.root
        for letter in word:
            if letter not in current.children:
                current.children[letter] = TrieNode()
            current = current.children[letter]
        current.is_end_of_word = True

    def search(self, word: str) -> bool:
        current = self.root
        for letter in word:
            if letter not in current.children:
                return False
            current = current.children[letter]
        return current.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        current = self.root
        for letter in prefix:
            if letter not in current.children:
                return False
            current = current.children[letter]
        return True


class Animation208(Scene):
    def construct(self):

        # Title
        title = Text("Trie (Prefix Tree) Implementation", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Our data structure
        self.trie = PrefixTree()
        self.node_positions = {}  # id(node) -> (x, y) position
        self.node_circles = {}  # id(node) -> Circle Mobject
        self.edges = []  # List of edges drawn

        # Root node - start from top left
        root_pos = np.array([-4, 2, 0])  # x,y,z
        self.node_positions[id(self.trie.root)] = root_pos
        root_circle = self.create_node_mobject("root", root_pos)
        self.node_circles[id(self.trie.root)] = root_circle

        # Animate the creation of root
        self.play(FadeIn(root_circle))

        # We'll define a set of operations and animate them step by step
        operations = [
            ("insert", "dog"),
            ("search", "do"),  # Return False
            ("startsWith", "do"),
            ("search", "dog"),  # Return True
        ]

        # Running offsets for new children, to place them diagonally
        self.next_child_x = -4  # Start closer to root
        self.next_child_y = 2  # Start at same level as root

        for op, argument in operations:
            # Show operation text
            operation_text = Text(f"{op}({argument})", font_size=28).next_to(
                root_circle, RIGHT, buff=2
            )
            self.play(Write(operation_text))

            if op == "insert":
                self.animate_insert(argument, operation_text)
            elif op == "search":
                result = self.trie.search(argument)
                self.animate_search(argument, result, operation_text)
            elif op == "startsWith":
                result = self.trie.startsWith(argument)
                self.animate_search(argument, result, operation_text, search_mode=False)

            # Remove operation text so next step is clear
            self.play(FadeOut(operation_text))
            self.wait(0.5)

        self.wait(2)

    def animate_insert(self, word, label_mobject):
        """
        Animate insertion of 'word' into the trie data structure,
        building new edges/nodes as needed and marking end-of-word.
        """
        current = self.trie.root

        for letter in word:
            # If letter not in current node's children, create a new node
            if letter not in current.children:
                current.children[letter] = TrieNode()
                new_node = current.children[letter]

                # Position new node diagonally down and right
                self.next_child_x += 1.5
                self.next_child_y -= 1.5
                child_pos = np.array([self.next_child_x, self.next_child_y, 0])
                self.node_positions[id(new_node)] = child_pos

                # create node circle
                node_circle = self.create_node_mobject(letter, child_pos)
                self.node_circles[id(new_node)] = node_circle

                # draw edge from current node to new child (without label)
                edge = Line(self.node_positions[id(current)], child_pos, color=WHITE)
                self.edges.append(((id(current), letter), edge))
                self.play(FadeIn(node_circle), Create(edge))
            else:
                # letter found; highlight the existing edge and node
                child_node = current.children[letter]
                edge = self.get_edge_mobject(current, letter)
                node_circle_mobj = self.node_circles[id(child_node)]

                highlight_edge = edge.copy().set_color(DARK_BLUE)
                self.play(Transform(edge, highlight_edge), run_time=0.5)
                self.play(
                    Transform(edge, edge.copy().set_color(WHITE)),
                    run_time=0.5,
                )

                highlight_node = node_circle_mobj.copy().set_color(DARK_BLUE)
                self.play(Transform(node_circle_mobj, highlight_node), run_time=0.5)
                self.play(
                    Transform(
                        node_circle_mobj, node_circle_mobj.copy().set_color(WHITE)
                    ),
                    run_time=0.5,
                )

            current = current.children[letter]

        # Mark end_of_word
        current.is_end_of_word = True
        node_circle = self.node_circles[id(current)]
        highlight_node = node_circle.copy().set_color(GREEN)
        self.play(Transform(node_circle, highlight_node), run_time=0.5)
        self.play(
            Transform(node_circle, node_circle.copy().set_color(WHITE)), run_time=0.5
        )

    def animate_search(self, word, result, label_mobject, search_mode=True):
        """
        Animate searching for 'word'.
          If search_mode=True, it is a full 'search',
          else it's a 'startsWith'.
        'result' is a bool indicating if the search succeeded.
        """
        current = self.trie.root
        for letter in word:
            if letter in current.children:
                # highlight the edge and node
                edge = self.get_edge_mobject(current, letter)
                child_node = current.children[letter]
                node_circle_mobj = self.node_circles[id(child_node)]
                #
                highlight_edge = edge.copy().set_color(DARK_BLUE)
                self.play(Transform(edge, highlight_edge), run_time=0.5)
                self.play(
                    Transform(edge, edge.copy().set_color(WHITE)),
                    run_time=0.5,
                )

                highlight_node = node_circle_mobj.copy().set_color(DARK_BLUE)
                self.play(Transform(node_circle_mobj, highlight_node), run_time=0.5)
                self.play(
                    Transform(
                        node_circle_mobj, node_circle_mobj.copy().set_color(WHITE)
                    ),
                    run_time=0.5,
                )

                current = child_node
            else:
                # fail
                fail_text = Text("Not found", color=RED, font_size=28).next_to(
                    label_mobject, DOWN, buff=0.2
                )
                self.play(Write(fail_text))
                self.wait(1)
                self.play(FadeOut(fail_text))
                return  # stop

        # If we finish the loop, check is_end_of_word if search_mode
        if search_mode:
            if current.is_end_of_word:
                success_text = Text("Found", color=GREEN, font_size=28).next_to(
                    label_mobject, DOWN, buff=0.2
                )
                self.play(Write(success_text))
                self.wait(1)
                self.play(FadeOut(success_text))
            else:
                fail_text = Text("Not end of word", color=RED, font_size=28).next_to(
                    label_mobject, DOWN, buff=0.2
                )
                self.play(Write(fail_text))
                self.wait(1)
                self.play(FadeOut(fail_text))
        else:
            # startsWith
            success_text = Text(
                "Prefix exists" if result else "Prefix not found",
                color=GREEN if result else RED,
                font_size=28,
            ).next_to(label_mobject, DOWN, buff=0.2)
            self.play(Write(success_text))
            self.wait(1)
            self.play(FadeOut(success_text))

    # -----------------------------------------------------------------
    # HELPER methods for drawing
    # -----------------------------------------------------------------
    def create_node_mobject(self, label, position):
        """
        Create a small circle with the given label (string) above it.
        Return a VGroup (circle + letter).
        """
        circle = Circle(radius=0.3, color=WHITE)
        circle.move_to(position)
        text = Text(str(label), font_size=22).move_to(position)
        return VGroup(circle, text)

    def create_edge(self, parent_pos, child_pos, letter):
        """
        Create a line from parent_pos to child_pos.
        Returns the Line mobject.
        """
        line = Line(parent_pos, child_pos, color=WHITE)
        self.edges.append(((id(parent_pos), letter), line))
        return line

    def get_edge_mobject(self, parent_node, letter):
        """
        Return the line mobject for the given parent's edge labeled 'letter'.
        """
        parent_pos = self.node_positions[id(parent_node)]
        for (p_id_letter), line in self.edges:
            if p_id_letter[1] == letter:
                return line
        return Line(ORIGIN, ORIGIN)  # fallback
