from manim import *

class GroupAnagrams(Scene):
    def construct(self):
        # Title
        title = Text("Group Anagrams Algorithm").scale(0.7).to_edge(UP)
        self.play(Write(title))

        # Example input
        strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

        ################################################################
        # 1) Display the original input strings across the top of the screen
        ################################################################
        input_header = Text("Input:", font_size=28).to_edge(LEFT).shift(UP*2)
        self.play(Write(input_header))

        # Create a row of Text mobjects for each input string
        input_strings_group = VGroup()
        for i, s in enumerate(strs):
            txt = Text(s, font_size=28)
            txt.next_to(input_header, RIGHT, buff=1 + i*1.2)
            input_strings_group.add(txt)

        self.play(*[Write(obj) for obj in input_strings_group])

        ################################################################
        # 2) Prepare the dictionary heading: "Dictionary (sorted -> group)"
        ################################################################
        dict_header = Text("Dictionary (sorted -> group)", font_size=28).to_edge(LEFT).shift(DOWN*0.1)
        self.play(Write(dict_header))

        # We'll keep two structures:
        #   dict_data   -> for logic  (Python dict: {sorted_key: [words]})
        #   dict_entries-> for visuals (Manim: {sorted_key: Text()})
        dict_data = {}
        self.dict_entries = {}

        # We'll place new dictionary lines one after another
        dict_y_offset = dict_header.get_center()[1] - 0.8

        # For highlighting each processed string
        highlight_rect = None

        ################################################################
        # 3) Iterate through each string, add to our dict, update display
        ################################################################
        for i, s in enumerate(strs):
            # Highlight the current string in blue
            if highlight_rect:
                self.play(FadeOut(highlight_rect))
            highlight_rect = SurroundingRectangle(
                input_strings_group[i], color=BLUE, buff=0.1
            )
            self.play(Create(highlight_rect))

            # "Sorting" demonstration text
            sorted_s = "".join(sorted(s))
            sorting_text = Text(
                f"Sorted: {sorted_s}",
                font_size=24
            ).next_to(input_strings_group[i], DOWN)
            self.play(Write(sorting_text))
            self.wait(0.6)
            self.play(FadeOut(sorting_text))

            # Update the Python dictionary
            if sorted_s not in dict_data:
                # It's the first word for this sorted key
                dict_data[sorted_s] = [s]

                # Create new line in the displayed "dictionary"
                display_str = f"{sorted_s}: [{s}]"
                new_line = Text(display_str, font_size=26)
                new_line.move_to([ -2.5, dict_y_offset, 0 ])
                self.play(Write(new_line))

                # Store reference to this text object
                self.dict_entries[sorted_s] = new_line
                dict_y_offset -= 0.6

            else:
                # Append the new word to the existing group
                dict_data[sorted_s].append(s)
                # Build the new displayed text from the updated group
                group_content = ", ".join(dict_data[sorted_s])
                new_line_str = f"{sorted_s}: [{group_content}]"
                new_line = Text(new_line_str, font_size=26)

                old_line = self.dict_entries[sorted_s]
                self.remove(old_line)

                new_line.move_to(old_line.get_center())

                # Transform old line into new line
                self.play(Write(new_line))

                # Update reference
                self.dict_entries[sorted_s] = new_line

        # Remove the last highlight
        if highlight_rect:
            self.play(FadeOut(highlight_rect))

        ################################################################
        # 4) Final display: Show the combined groups at the bottom
        ################################################################
        final_groups_header = Text("Final Groups:", font_size=28).to_edge(LEFT).shift(DOWN*3.5)
        self.play(Write(final_groups_header))

        # Construct the final list-of-lists from our dict_data
        all_groups = list(dict_data.values())
        final_groups_str = "[" + ", ".join(str(group) for group in all_groups) + "]"
        final_groups_text = Text(final_groups_str, font_size=28)
        final_groups_text.next_to(final_groups_header, RIGHT, buff=0.3)
        self.play(Write(final_groups_text))

        # Pause before ending
        self.wait(2)