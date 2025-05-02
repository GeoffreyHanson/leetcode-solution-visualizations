############################################################################
#      Tortoise‑and‑Hare cycle demo: 2 linear nodes, 5‑node cycle          #
############################################################################

import numpy as np
from manim import *


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.mobj = None  # Manim graphic for the node


class CycleDetection(Scene):
    def construct(self):
        ####################################################################
        # 1) Build list: 1 → 2 → 3 → 4 → 5 → 6 → 7
        #                           ↖─────────────┘ (cycle 3‑4‑5‑6‑7‑3)
        ####################################################################
        nodes = [ListNode(i) for i in range(1, 8)]
        for a, b in zip(nodes, nodes[1:]):
            a.next = b
        nodes[-1].next = nodes[2]  # node 7 points back to node 3
        head = nodes[0]

        ####################################################################
        # 2) Lay out graphics
        #    – nodes 1‑2 in a line on the left
        #    – nodes 3‑7 in a pentagon on the right
        ####################################################################
        tail_positions = [(-6, 0, 0), (-4, 0, 0)]  # nodes 1,2
        R = 3
        cycle_angles = np.linspace(PI / 2, PI / 2 - 2 * PI, 5, endpoint=False)
        cycle_positions = [
            (R * np.cos(a) + 1, R * np.sin(a), 0) for a in cycle_angles
        ]  # nodes 3‑7
        positions = tail_positions + cycle_positions

        # draw nodes
        node_group = VGroup()
        for nd, pos in zip(nodes, positions):
            circ = Circle(radius=0.4, color=WHITE).move_to(pos)
            label = Text(str(nd.val), font_size=26).move_to(pos)
            nd.mobj = VGroup(circ, label)
            node_group.add(nd.mobj)

        # draw arrows
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            # Vector pointing from current node to next node
            direction_vector = (
                positions[i + 1][0] - positions[i][0],
                positions[i + 1][1] - positions[i][1],
                0,
            )

            arrows.add(
                Arrow(
                    start=nodes[i].mobj.get_center(),
                    end=nodes[i + 1].mobj.get_center(),
                    buff=0.4,  # Buffer at both ends
                    stroke_width=2,
                )
            )
        # arrow 7 → 3 (cycle back edge)
        arrows.add(
            Arrow(
                start=nodes[6].mobj.get_center(),
                end=nodes[2].mobj.get_center(),
                buff=0.4,  # Buffer at both ends
                stroke_width=2,
                color=YELLOW,
            )
        )

        # Title
        title = Text("Cycle detection with tail", font_size=34).to_edge(UP)
        self.play(Write(title))
        self.play(FadeIn(node_group), Create(arrows))
        self.wait(0.5)

        ####################################################################
        # 3) Slow & Fast pointers
        ####################################################################
        slow_dot = Dot(color=BLUE, radius=0.15).move_to(nodes[0].mobj)
        fast_dot = Dot(color=RED, radius=0.15).move_to(nodes[0].mobj)
        slow_lab = Text("slow", font_size=20, color=BLUE).next_to(slow_dot, DOWN, 0.5)
        fast_lab = Text("fast", font_size=20, color=RED).next_to(fast_dot, UP, 0.5)
        self.play(FadeIn(slow_dot, fast_dot, slow_lab, fast_lab))
        self.wait(0.5)

        ####################################################################
        # 4) Floyd's algorithm (slow pace)
        ####################################################################
        slow = fast = head
        found = False
        while True:
            # advance pointers
            slow = slow.next
            fast = fast.next.next

            # animate moves
            self.play(
                slow_dot.animate.move_to(slow.mobj),
                fast_dot.animate.move_to(fast.mobj),
                run_time=1.5,
                rate_func=linear,
            )

            if slow is fast:
                found = True
                meet_flash = slow.mobj.copy().set_color(GREEN).set(opacity=0.4)
                self.play(FadeIn(meet_flash.scale(1.4)), run_time=0.6)
                self.play(FadeOut(meet_flash))
                break

        ####################################################################
        # 5) Result
        ####################################################################
        result = Text("Cycle Detected!", font_size=32, color=GREEN).to_edge(DOWN)
        self.play(Write(result))
        self.wait(2)
