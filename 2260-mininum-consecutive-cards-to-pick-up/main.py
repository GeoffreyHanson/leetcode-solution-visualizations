from manim import *


class MinConsecutiveCards(Scene):
    def construct(self):
        # Title
        title = (
            Text("Minimum Consecutive Cards to Pick Up for a Matching Pair")
            .scale(0.65)
            .to_edge(UP)
        )
        self.play(Write(title))

        # Example input
        cards = [3, 4, 2, 3, 4, 7]

        # 1) Display the input array (row of squares labeled with values)
        array_group = self.create_card_array(cards)
        array_group.shift(UP * 1)  # move it higher if needed
        self.play(FadeIn(array_group))

        # Prepare a dictionary heading: "Last Seen Dict (card -> last index)"
        dict_header = (
            Text("Last Seen Dict (card: last index)", font_size=28)
            .to_edge(LEFT)
            .shift(DOWN * 1.5)
        )
        self.play(Write(dict_header))

        # We'll keep these:
        #   seen_data: A plain Python dict tracking card -> last index
        #   dict_entries: A map from card -> the Manim Text() line we show on screen
        seen_data = {}
        dict_entries = {}
        dict_y_offset = (
            dict_header.get_center()[1] - 0.7
        )  # place dictionary lines below header

        # For highlighting the current card
        highlight_rect = None

        # Keep track of min_draws and a text object to show it
        min_draws = float("inf")
        min_draws_title = Text("min_draws:", font_size=28).to_edge(RIGHT).shift(UP * 1)
        self.play(Write(min_draws_title))
        min_draws_text = Text("∞", font_size=28)
        min_draws_text.next_to(min_draws_title, DOWN, buff=0.2)
        self.play(Write(min_draws_text))

        # We'll store references for subarray highlights so we can fade them out
        current_subarray_highlight = None

        # 2) Iterate through cards
        for i, card_val in enumerate(cards):
            # Highlight the current square
            if highlight_rect:
                self.play(FadeOut(highlight_rect))
            current_card_mobj = array_group[
                2 * i
            ]  # squares at even indices in the group
            highlight_rect = SurroundingRectangle(
                current_card_mobj, color=BLUE, buff=0.05
            )
            self.play(Create(highlight_rect))

            # If we've seen this card before, compute distance
            if card_val in seen_data:
                # subarray size is (i - seen[card_val] + 1)
                prev_index = seen_data[card_val]
                draws = i - prev_index + 1

                # If we have a leftover highlight from the previous match, remove it
                if current_subarray_highlight:
                    self.play(FadeOut(current_subarray_highlight))

                # Highlight the subarray from prev_index to i
                subarray_mobjects = VGroup(
                    *[array_group[2 * j] for j in range(prev_index, i + 1)]
                )
                current_subarray_highlight = SurroundingRectangle(
                    subarray_mobjects, color=YELLOW, buff=0.07
                )
                self.play(Create(current_subarray_highlight))

                # Update min_draws if needed
                if draws < min_draws:
                    min_draws = draws
                    # Animate changing text from the old value to new
                    new_min_text = Text(str(min_draws), font_size=28)
                    new_min_text.move_to(min_draws_text.get_center())
                    self.play(Transform(min_draws_text, new_min_text))

            # Update "seen" dictionary with the current card index
            seen_data[card_val] = i

            # Update or create a dictionary entry text on the right
            if card_val not in dict_entries:
                # new line
                entry_str = f"{card_val}: {i}"
                entry_text = Text(entry_str, font_size=26)
                entry_text.move_to([-2.5, dict_y_offset, 0])
                self.play(Write(entry_text))
                dict_entries[card_val] = entry_text
                dict_y_offset -= 0.5
            else:
                # transform the existing line
                old_text = dict_entries[card_val]
                new_line_str = f"{card_val}: {i}"
                new_text_mobj = Text(new_line_str, font_size=26)
                new_text_mobj.move_to(old_text.get_center())
                self.play(Transform(old_text, new_text_mobj))
                dict_entries[card_val] = new_text_mobj

        # Remove the final highlight
        if highlight_rect:
            self.play(FadeOut(highlight_rect))

        # 3) Show the final result
        if min_draws == float("inf"):
            result_str = "No matching cards found. (-1)"
        else:
            result_str = f"Minimum subarray length = {min_draws}"

        result_text = Text(result_str, font_size=30, color=GREEN).next_to(
            array_group, DOWN, buff=1
        )
        self.play(Write(result_text))

        # Pause before ending
        self.wait(2)

    def create_card_array(self, cards):
        """
        Create a row of squares labeled with each card value.
        Return a VGroup: [Square(0), Text(0), Square(1), Text(1), ...].
        The squares are at even indices, the text at odd indices.
        """
        group = VGroup()
        for i, val in enumerate(cards):
            square = Square(side_length=0.6)
            square.shift(RIGHT * i * 1.1)
            text = Text(str(val), font_size=24).move_to(square.get_center())
            group.add(square, text)

        group.move_to(ORIGIN)
        return group

