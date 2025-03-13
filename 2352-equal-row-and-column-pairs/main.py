from collections import Counter

from manim import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    YELLOW,
    Create,
    FadeIn,
    FadeOut,
    Scene,
    Square,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
    Write,
)


class EqualPairsExplanation(Scene):
    def construct(self):
        # 1) Title
        title = Text("Equal Pairs of Rows and Columns", font_size=32).to_edge(UP)
        self.play(Write(title))

        # Example grid
        grid = [
            [1, 2, 3],
            [2, 2, 2],
            [1, 2, 3],
        ]

        # Create squares for the grid
        grid_mobjects = self.create_grid_mobjects(grid)
        grid_group = VGroup(*[mobj for row in grid_mobjects for mobj in row])
        grid_group.move_to(ORIGIN).shift(UP*1.5)
        self.play(FadeIn(grid_group))

        #######################################################################
        # 2) Build row_count, storing row_squares in self.row_squares_map
        #######################################################################
        row_header = Text("row_count (row: freq)", font_size=28)
        row_header.next_to(grid_group, LEFT).to_edge(LEFT)
        self.play(Write(row_header))

        row_count = Counter()
        row_entries = VGroup()
        self.add(row_entries)

        self.row_lines = {}        # (row_tuple) -> Text Mobject
        self.row_squares_map = {}  # (row_tuple) -> VGroup of squares for that row

        highlight_rect = None
        for r_idx, row in enumerate(grid):
            # Highlight the row squares in BLUE
            if highlight_rect:
                self.play(FadeOut(highlight_rect))
            row_squares = VGroup(*[grid_mobjects[r_idx][c_idx] for c_idx in range(len(row))])
            highlight_rect = SurroundingRectangle(row_squares, color=BLUE, buff=0.1)
            self.play(Create(highlight_rect))

            row_tuple = tuple(row)
            row_count[row_tuple] += 1

            # Store squares for this row_tuple
            self.row_squares_map[row_tuple] = row_squares

            # Update or create row_count display line
            self.update_counter_display(
                header=row_header,
                counter_group=row_entries,
                current_dict=row_count,
                key=row_tuple,
                line_map=self.row_lines,
            )

        self.play(FadeOut(highlight_rect))

        #######################################################################
        # 3) Build col_count, storing col_squares in self.col_squares_map
        #######################################################################
        col_header = Text("col_count (col: freq)", font_size=28)
        col_header.next_to(row_entries, DOWN, buff=1).align_to(row_header, LEFT)
        self.play(Write(col_header))

        col_count = Counter()
        col_entries = VGroup()
        self.add(col_entries)

        self.col_lines = {}        # (col_tuple) -> Text Mobject
        self.col_squares_map = {}  # (col_tuple) -> VGroup of squares for that column

        num_rows = len(grid)
        num_cols = len(grid[0])
        for c_idx in range(num_cols):
            # squares for the c_idx-th column
            col_squares = VGroup(*[grid_mobjects[r_idx][c_idx] for r_idx in range(num_rows)])
            highlight_rect = SurroundingRectangle(col_squares, color=BLUE, buff=0.1)
            self.play(Create(highlight_rect))

            col_tuple = tuple(grid[r][c_idx] for r in range(num_rows))
            col_count[col_tuple] += 1

            # Store squares for this col_tuple
            self.col_squares_map[col_tuple] = col_squares

            # Update or create col_count display line
            self.update_counter_display(
                header=col_header,
                counter_group=col_entries,
                current_dict=col_count,
                key=col_tuple,
                line_map=self.col_lines,
            )

            self.play(FadeOut(highlight_rect))

        #######################################################################
        # 4) Summation: highlight row+col lines *and* their squares in YELLOW
        #######################################################################
        sum_header = Text("Equal Row and Column Pairs:", font_size=28)
        sum_header.next_to(grid_group, DOWN)
        self.play(Write(sum_header))

        result_so_far = 0
        sum_text = Text(f"{result_so_far}", font_size=28).next_to(sum_header, RIGHT, buff=0.3)
        self.play(Write(sum_text))

        for key in row_count:
            if key in col_count:
                pairs_found = row_count[key] * col_count[key]
                if pairs_found > 0:
                    # Retrieve actual line Mobjects
                    row_line = self.row_lines.get(key)
                    col_line = self.col_lines.get(key)
                    # Retrieve squares for that row & col
                    row_squares = self.row_squares_map.get(key)
                    col_squares = self.col_squares_map.get(key)

                    # Create highlight rectangles if they exist
                    row_line_high = SurroundingRectangle(row_line, color=YELLOW, buff=0.1) if row_line else None
                    col_line_high = SurroundingRectangle(col_line, color=YELLOW, buff=0.1) if col_line else None
                    row_squares_high = SurroundingRectangle(row_squares, color=YELLOW, buff=0.1) if row_squares else None
                    col_squares_high = SurroundingRectangle(col_squares, color=YELLOW, buff=0.1) if col_squares else None

                    # Gather all highlight animations
                    anims_in = []
                    if row_line_high:    anims_in.append(Create(row_line_high))
                    if col_line_high:    anims_in.append(Create(col_line_high))
                    if row_squares_high: anims_in.append(Create(row_squares_high))
                    if col_squares_high: anims_in.append(Create(col_squares_high))

                    # Animate them simultaneously
                    if anims_in:
                        self.play(*anims_in)
                        self.wait(0.3)

                    # Update partial sum
                    new_result = result_so_far + pairs_found
                    new_sum_text_obj = Text(str(new_result), font_size=28).move_to(sum_text.get_center())
                    self.play(Transform(sum_text, new_sum_text_obj))
                    result_so_far = new_result

                    # Remove highlights
                    anims_out = []
                    if row_line_high:    anims_out.append(FadeOut(row_line_high))
                    if col_line_high:    anims_out.append(FadeOut(col_line_high))
                    if row_squares_high: anims_out.append(FadeOut(row_squares_high))
                    if col_squares_high: anims_out.append(FadeOut(col_squares_high))
                    if anims_out:
                        self.play(*anims_out)

        # 5) Final result
        # final_str = f"Equal Row and Column Pairs = {result_so_far}"
        # final_text = Text(final_str, font_size=30, color=GREEN)
        # final_text.next_to(sum_header, DOWN, buff=1)
        # self.play(Write(final_text))

        # self.wait(2)


    ############################################################################
    # Helper methods
    ############################################################################
    def create_grid_mobjects(self, grid):
        """
        Convert a 2D list of ints into VGroups of squares+text.
        grid_mobjects[r][c] = VGroup(Square, Text)
        """
        nrows = len(grid)
        ncols = len(grid[0])
        cell_mobjects = []
        for r in range(nrows):
            row_mobjs = []
            for c in range(ncols):
                val = grid[r][c]
                square = Square(side_length=0.6)
                square.shift(RIGHT * c * 0.65 + DOWN * r * 0.65)
                text_mobj = Text(str(val), font_size=24).move_to(square.get_center())
                row_mobjs.append(VGroup(square, text_mobj))
            cell_mobjects.append(row_mobjs)
        return cell_mobjects

    def update_counter_display(self, header, counter_group, current_dict, key, line_map):
        """
        For the given 'key', display or update "key: freq" in 'counter_group'.
        Also store the resulting Text Mobject in line_map[key].
        """
        freq = current_dict[key]
        entry_str = f"{key}: {freq}"

        # If we already have a text line for this key, transform it
        if key in line_map:
            old_line = line_map[key]
            new_line_mobj = Text(entry_str, font_size=24)
            new_line_mobj.move_to(old_line.get_center())
            self.play(Transform(old_line, new_line_mobj))
            line_map[key] = new_line_mobj
        else:
            # Create a new line
            new_line = Text(entry_str, font_size=24)
            if len(counter_group) == 0:
                new_line.next_to(header, DOWN, buff=0.3).align_to(header, LEFT)
            else:
                new_line.next_to(counter_group[-1], DOWN, buff=0.2).align_to(header, LEFT)
            counter_group.add(new_line)
            self.play(Write(new_line))
            line_map[key] = new_line