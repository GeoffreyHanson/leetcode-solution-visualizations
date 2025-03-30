from collections import Counter

import numpy as np
from manim import *


class Animation771(Scene):
    def construct(self):
        # Title
        title = Text("Jewels and Stones", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Input strings
        jewels_str = "aA"
        stones_str = "aAAbbbb"

        # Display input strings
        jewels_text = (
            Text(f"Jewels: {jewels_str}", font_size=28).to_edge(LEFT).shift(UP * 2)
        )
        stones_text = (
            Text(f"Stones: {stones_str}", font_size=28)
            .next_to(jewels_text, DOWN, buff=0.5)
            .align_to(jewels_text, LEFT)
        )
        self.play(Write(jewels_text), Write(stones_text))

        # Create and display the jewels set (as a text)
        jewel_set = set(jewels_str)
        # Sort for consistent order (optional)
        sorted_jewels = ", ".join(sorted(jewel_set))
        jewels_set_text = (
            Text(f"Jewels Set: {{{sorted_jewels}}}", font_size=28)
            .next_to(stones_text, DOWN, buff=1)
            .align_to(stones_text, LEFT)
        )
        self.play(Write(jewels_set_text))

        # Create boxes for the stones
        stones_boxes = self.create_boxes(stones_str)
        # Position them on the right side below the input texts
        stones_boxes.next_to(jewels_set_text, RIGHT, buff=2)
        self.play(FadeIn(stones_boxes))

        # Create a running count display
        count = 0
        count_text = (
            Text("Count: 0", font_size=28)
            .next_to(stones_boxes, DOWN, buff=1)
            .align_to(stones_boxes, LEFT)
        )
        self.play(Write(count_text))

        # Process each stone (each stone is represented as a VGroup: [Square, Letter Text])
        for i, box in enumerate(stones_boxes):
            # Get the letter from the box (we assume box[1] is the Text object)
            letter = box[1].text

            # Highlight the current stone's box in yellow
            highlight = SurroundingRectangle(box, color=YELLOW, buff=0.1)
            self.play(Create(highlight), run_time=0.3)

            # Check membership: if stone is a jewel, mark green; else red
            if letter in jewel_set:
                count += 1
                self.play(box.animate.set_color(GREEN), run_time=0.3)
            else:
                self.play(box.animate.set_color(RED), run_time=0.3)

            self.play(FadeOut(highlight), run_time=0.2)

            # Update the count text
            new_count_text = Text(f"Count: {count}", font_size=28).move_to(
                count_text.get_center()
            )
            self.play(Transform(count_text, new_count_text), run_time=0.3)

        # Show final result
        result_text = Text(f"Result: {count}", font_size=36, color=GREEN).next_to(
            count_text, DOWN, buff=1
        )
        self.play(Write(result_text))

        self.wait(2)

    def create_boxes(self, s):
        """
        Create a VGroup of boxes for each character in s.
        Each box is a VGroup containing a Square and a centered Text.
        Returns a VGroup arranged horizontally.
        """
        boxes = VGroup()
        # Use a fixed buff; adjust as needed
        buff = 1.0
        for i, ch in enumerate(s):
            square = Square(side_length=0.8, color=WHITE)
            letter_text = Text(ch, font_size=36)
            group = VGroup(square, letter_text)
            # Center the letter on the square
            letter_text.move_to(square.get_center())
            # Position each box horizontally
            group.move_to(np.array([i * buff, 0, 0]))
            boxes.add(group)
        boxes.center()  # center the whole group
        return boxes
