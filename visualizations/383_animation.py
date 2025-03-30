from collections import Counter

from manim import *


class CanConstructExplanation(Scene):
    def construct(self):
        ###################################################################
        # 1) Example strings
        ###################################################################
        # ransom_note = "leet"
        ransom_note = "bg"
        # magazine = "lleeet"  # repeated letters: l ->2, e->3, t->1
        magazine = "efjbdfbdgfjhhaiigfhbaeja"

        ###################################################################
        # 2) Title
        ###################################################################
        title = Text("Ransom Note", font_size=36).to_edge(UP)
        self.play(Write(title))

        ###################################################################
        # 3) Ransom Note Row: one square per character
        ###################################################################
        ransom_header = Text("Ransom Note", font_size=28)
        ransom_squares = self.create_string_boxes(ransom_note, buff=0.6)

        ransom_header.to_edge(LEFT).shift(UP * 2.5)
        ransom_squares.next_to(ransom_header, RIGHT, buff=1)

        self.play(Write(ransom_header), FadeIn(ransom_squares))

        ###################################################################
        # 4) Magazine Row: only one square per distinct letter
        ###################################################################
        magazine_header = Text("Magazine (Letter: Count)", font_size=28)
        magazine_header.next_to(ransom_header, DOWN, buff=2).align_to(
            ransom_header, LEFT
        )
        self.play(Write(magazine_header))

        # Build a Counter for the magazine
        mag_counter = Counter(magazine)

        # We'll create a row of squares, each holding a single letter & count
        # in the order they appear in the magazine, but skipping duplicates.
        # Or you could sort them, whichever you prefer:
        # unique_letters = list(dict.fromkeys(magazine))  # preserve order
        unique_letters = []
        for ch in magazine:
            if ch not in unique_letters:
                unique_letters.append(ch)

        # Build the squares
        magazine_group, mag_map = self.create_letter_count_boxes(
            unique_letters, mag_counter
        )
        # magazine_group is the entire row
        # mag_map is a dict { letter: (Square, letter_text, count_text) }

        magazine_group.next_to(magazine_header, DOWN, buff=1).align_to(
            magazine_header, LEFT
        )
        self.play(FadeIn(magazine_group))

        ###################################################################
        # 5) Animate the logic: for each letter in ransom_note
        ###################################################################
        highlight_rnote = None
        for i, r_sq in enumerate(ransom_squares[::2]):  # squares at even indices
            letter_text = ransom_squares[2 * i + 1]  # text inside that square
            letter = letter_text.text

            # 5a) Highlight the current Ransom Note letter in BLUE
            if highlight_rnote:
                self.play(FadeOut(highlight_rnote))
            highlight_rnote = SurroundingRectangle(r_sq, color=BLUE, buff=0.1)
            self.play(Create(highlight_rnote))

            # If magazine doesn't have enough of this letter, fail
            if mag_counter[letter] == 0:
                fail_box = SurroundingRectangle(letter_text, color=RED, buff=0.1)
                self.play(Create(fail_box))
                self.wait(1)
                self.play(FadeOut(fail_box))
                break  # or show some "Cannot Construct" message
            else:
                # Decrement
                old_count = mag_counter[letter]
                mag_counter[letter] -= 1
                new_count = mag_counter[letter]

                # 5b) Highlight the magazine square for that letter in YELLOW
                if letter in mag_map:
                    sq, l_txt, cnt_txt = mag_map[letter]
                    mag_high = SurroundingRectangle(sq, color=YELLOW, buff=0.1)
                    self.play(Create(mag_high))

                    # Animate transforming the count text
                    new_cnt_mobj = Text(str(new_count), font_size=20)
                    new_cnt_mobj.move_to(cnt_txt.get_center())
                    self.play(Transform(cnt_txt, new_cnt_mobj))

                    self.play(FadeOut(mag_high))

        # Remove last highlight
        if highlight_rnote:
            self.play(FadeOut(highlight_rnote))

        ###################################################################
        # 6) Final result text
        ###################################################################
        # Check if can construct
        can_construct = all(mag_counter[ch] >= 0 for ch in ransom_note)
        result_str = (
            "True: Can Construct" if can_construct else "False: Cannot Construct"
        )
        result_mobj = Text(
            result_str, font_size=30, color=GREEN if can_construct else RED
        )
        result_mobj.to_edge(DOWN)
        self.play(Write(result_mobj))

        self.wait(2)  # pause

    ###################################################################
    # Helper: create_string_boxes
    ###################################################################
    def create_string_boxes(self, text_str, buff=0.8):
        """
        Create a VGroup of squares+Text for each character, i.e.:
          [Square0, Text0, Square1, Text1, ...]
        """
        group = VGroup()
        for i, ch in enumerate(text_str):
            sq = Square(side_length=0.6)
            sq.shift(RIGHT * i * buff)
            txt = Text(ch, font_size=24).move_to(sq.get_center())
            group.add(sq, txt)
        group.move_to(ORIGIN)
        return group

    ###################################################################
    # Helper: create_letter_count_boxes
    ###################################################################
    def create_letter_count_boxes(self, letters, mag_counter):
        """
        Build a row of squares, each representing a unique letter from `letters`.
        Each square will contain two lines:
          - Large letter text at the top
          - Smaller count at the bottom
        We return:
           group, mag_map
        where `group` is the entire VGroup,
              `mag_map` is { letter -> (Square, letter_text, count_text) }.
        """
        group = VGroup()
        mag_map = {}
        buff = 1.0
        for i, letter in enumerate(letters):
            count = mag_counter[letter]
            sq = Square(side_length=1.0)
            sq.shift(RIGHT * i * buff)

            # Two texts: letter on top, count below
            letter_mobj = Text(letter, font_size=24)
            count_mobj = Text(str(count), font_size=20, color=WHITE)

            # Position them inside the square
            letter_mobj.move_to(sq.get_top() - UP * 0.3)
            count_mobj.move_to(sq.get_bottom() + UP * 0.3)

            # Combine
            cell = VGroup(sq, letter_mobj, count_mobj)
            group.add(cell)
            mag_map[letter] = (sq, letter_mobj, count_mobj)

        group.move_to(ORIGIN)
        return group, mag_map
