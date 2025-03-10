from manim import *


class MaxSumOfAPair(Scene):
    def construct(self):
        # Title
        title = (
            Text("Maximum Sum of Two Numbers With Equal Digit Sum")
            .scale(0.65)
            .to_edge(UP)
        )
        self.play(Write(title))

        # Example input: adjust as you wish
        nums = [51, 71, 17, 42]

        ###################################################################
        # 1) Display the input array
        ###################################################################
        input_header = Text("Input:", font_size=28)
        input_header.to_edge(LEFT).shift(UP * 2)
        self.play(Write(input_header))

        array_group = self.create_array_visual(nums)
        array_group.next_to(input_header, RIGHT, buff=0.5)
        self.play(FadeIn(array_group))

        ###################################################################
        # 2) Dictionary heading: "digit_sum -> largest number"
        ###################################################################
        dict_header = Text("Map: digit_sum -> largest number", font_size=26)
        # Place it below the array, shifted to the left
        dict_header.to_edge(LEFT).align_to(input_header, LEFT).shift(DOWN * 1.5)
        self.play(Write(dict_header))

        # We'll keep a dictionary for the data, and a map from digit_sum -> mobject
        sums_dict = {}
        dict_entries = (
            VGroup()
        )  # We'll store all lines in a VGroup for easier positioning
        self.add(dict_entries)  # Add it to the scene so we can keep building below

        ###################################################################
        # 3) max_sum text display on the right side
        ###################################################################
        max_sum_header = Text("max_sum:", font_size=28)
        max_sum_header.to_edge(RIGHT).shift(UP * 2)
        self.play(Write(max_sum_header))

        max_sum_val = -1
        max_sum_text = Text(str(max_sum_val), font_size=28)
        max_sum_text.next_to(max_sum_header, DOWN, buff=0.2)
        self.play(Write(max_sum_text))

        ###################################################################
        # 4) Iterate through nums, compute digit sum, update dictionary & max_sum
        ###################################################################
        highlight_rect = None

        for i, num in enumerate(nums):
            # Highlight the current square
            if highlight_rect:
                self.play(FadeOut(highlight_rect))
            current_square = array_group[2 * i]
            highlight_rect = SurroundingRectangle(current_square, color=BLUE, buff=0.05)
            self.play(Create(highlight_rect))

            # Show digit sum
            ds = self.get_digit_sum(num)
            ds_text = Text(f"digit_sum({num}) = {ds}", font_size=24).next_to(
                current_square, DOWN
            )
            self.play(Write(ds_text))
            self.wait(0.6)
            self.play(FadeOut(ds_text))

            # If we already have a number with this digit sum, check potential new sum
            if ds in sums_dict:
                old_num = sums_dict[ds]
                cur_sum = old_num + num
                if cur_sum > max_sum_val:
                    max_sum_val = cur_sum
                    new_max_sum_text = Text(str(max_sum_val), font_size=28).move_to(
                        max_sum_text.get_center()
                    )
                    self.play(Transform(max_sum_text, new_max_sum_text))

                # Update dictionary to store the larger number if this num is bigger
                if num > sums_dict[ds]:
                    sums_dict[ds] = num
                    self.update_dict_line(dict_header, dict_entries, ds, num)
            else:
                sums_dict[ds] = num
                # Create a new line under the dictionary heading
                self.create_dict_line(dict_header, dict_entries, ds, num)

        # Remove highlight
        if highlight_rect:
            self.play(FadeOut(highlight_rect))

        ###################################################################
        # 5) Show final max_sum at the bottom
        ###################################################################
        final_text_str = (
            f"Final max_sum = {max_sum_val}"
            if max_sum_val > -1
            else "No valid pairs found."
        )
        final_text = Text(final_text_str, font_size=28, color=GREEN)
        final_text.next_to(array_group, DOWN, buff=1).to_edge(LEFT)
        self.play(Write(final_text))

        self.wait(2)

    def create_array_visual(self, nums):
        """
        Create a row of squares labeled with each value in nums.
        Return a VGroup: [Square(0), Text(0), Square(1), Text(1), ...].
        """
        group = VGroup()
        for i, val in enumerate(nums):
            square = Square(side_length=0.6)
            square.shift(RIGHT * i * 1.1)
            text = Text(str(val), font_size=24).move_to(square.get_center())
            group.add(square, text)
        group.move_to(ORIGIN)
        return group

    def get_digit_sum(self, num):
        """Return the sum of digits of num."""
        return sum(int(d) for d in str(num))

    def create_dict_line(self, dict_header, dict_entries, ds, val):
        """
        Create a new dictionary line "ds -> val" below the existing dictionary lines,
        starting below dict_header.
        """
        entry_str = f"{ds} -> {val}"
        new_line = Text(entry_str, font_size=24)
        # If there are no existing entries, place it under dict_header
        if len(dict_entries) == 0:
            new_line.next_to(dict_header, DOWN, buff=0.3)
        else:
            # Otherwise, place it below the last line in dict_entries
            last_line = dict_entries[-1]
            new_line.next_to(last_line, DOWN, buff=0.2)
        dict_entries.add(new_line)
        self.play(Write(new_line))

    def update_dict_line(self, dict_header, dict_entries, ds, val):
        """
        Update the existing line for 'ds -> ...' to reflect the new val,
        by transforming the text object in-place.
        """
        # Find the line with digit sum ds
        # For a small dictionary, we can just search it. Alternatively, keep a separate dict for references.
        for line in dict_entries:
            if line.text.startswith(f"{ds} ->"):
                old_line = line
                new_line_str = f"{ds} -> {val}"
                new_line = Text(new_line_str, font_size=24)
                new_line.move_to(old_line.get_center())
                self.play(Transform(old_line, new_line))
                return
