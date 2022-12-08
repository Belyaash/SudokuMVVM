import numpy as np


class SudokuState:
    # This class used from https://github.com/ouked/sudoku_solver

    # dict of constraints, RCV as keys
    get_constraints = {}
    length_of_block: int

    def __init__(self, values: np.ndarray, length_of_block=3):
        """
        Create a new Sudoku State.
        Calculates matrix A from passed values
        :param values: 9x9 grid of initial state
        """
        self.get_constraints.clear()
        self.length_of_block = length_of_block
        self.side = length_of_block**2
        self.populate_get_constrains()

        self.solvable = True
        self.solution = {}
        self.values = values

        # matrix A
        self.a = {
            c: set() for c in (
                # Every cell must contain a value, (col, row)
                    [("Cell", (x, y)) for x in range(self.side) for y in range(self.side)] +

                    # Every row must contain each value, (row, val)
                    [("Row", (row, val)) for row in range(self.side) for val in range(1, self.side+1)] +

                    # Every column must contain each value, (column, val)
                    [("Col", (col, val)) for col in range(self.side) for val in range(1, self.side+1)] +

                    # Every block must contain each value, (block, val)
                    [("Block", (blk, val)) for blk in range(self.side) for val in range(1, self.side+1)]
            )
        }

        # Populate A with the associated RCVs
        for rcv, consts in SudokuState.get_constraints.items():
            for c in consts:
                self.a[c].add(rcv)

        # Update constraints to reflect initial state
        for (y, x), value in np.ndenumerate(values):
            if value != 0:
                try:
                    self.remove_conflicting_rcvs((y, x, value))
                except KeyError:
                    self.solvable = False

    def populate_get_constrains(self):
        # Populate get_constraints
        for r in range(self.side):
            block_y = r // self.length_of_block

            for c in range(self.side):
                block_x = c // self.length_of_block
                b = (block_y * self.length_of_block) + block_x

                for v in range(1, self.side+1):
                    # Truncates r, c down to nearest multiple of 3
                    # Get block id
                    #   0 1 2
                    #   3 4 5
                    #   6 7 8

                    self.get_constraints[(r, c, v)] = [
                        # Every cell must have a value, (x, y)
                        ("Cell", (r, c)),
                        # Every row must contain each value, (row, val)
                        ("Row", (r, v)),
                        # Every column must contain each value, (column, val)
                        ("Col", (c, v)),
                        # Every block must contain each value, (block, val)
                        ("Block", (b, v))
                    ]

    def remove_conflicting_rcvs(self, rcv: (int, int, int)):
        """
        Removes RCV from other constraints
        :param rcv: Row, Column, Value tuple to look up
        :return: list of removed RCVs
        """
        # This is pretty nasty, but can't think of another way of doing it. Maybe pd.dataframes?

        # List of removed RCVs (so they can be restored later)
        removed_rcvs = []

        # For constraint RCV satisfies
        for c in SudokuState.get_constraints[rcv]:

            # For other RCV that ALSO satisfy c
            for other_rcv in self.a[c]:

                # For other constraints that the other RCV satisfies
                for other_c in SudokuState.get_constraints[other_rcv]:

                    # Remove other_rcv from the other constraint
                    if other_c != c:
                        self.a[other_c].remove(other_rcv)

            removed_rcvs.append(self.a.pop(c))

        return removed_rcvs

    def restore_rcvs(self, rcv: (int, int, int), removed):
        """
        Undoes the affect of remove_conflicting_rcvs. Adds RCVs back to their constraints.
        :param rcv: Row, Column, Value that was used to remove values
        :param removed: Removed columns to restore
        :return: None
        """
        # removed is an ordered list, so we must work backwards
        for c in reversed(SudokuState.get_constraints[rcv]):
            # Get column from list
            self.a[c] = removed.pop()
            # For other rcv that satisfy c
            for other_rcv in self.a[c]:
                # For other constraints that the other rcv satisfies
                for other_c in SudokuState.get_constraints[other_rcv]:
                    self.a[other_c].add(other_rcv)

    def add_solution(self, rcv: (int, int, int)):
        """
        Add the given RCV to solutions, and remove associated RCVs from matrix
        :param rcv: Row, Column, Value tuple to add to solution
        :return: Removed RCVs
        """
        r, c, v = rcv
        self.solution[(r, c)] = v

        removed_rcvs = self.remove_conflicting_rcvs(rcv)

        return removed_rcvs

    def remove_solution(self, rcv: (int, int, int), removed):
        """
        Remove the given RCV from solutions, and restores associated RCVs to matrix
        :param removed:
        :param rcv: Row, Column, Value tuple to add to solution
        :return: Updated solutions
        """
        r, c, v = rcv
        del self.solution[r, c]
        self.restore_rcvs(rcv, removed)
        return self.solution

    def pick_constraint(self) -> ((str, (int, int, int)), set):
        """
        Picks the next non-empty constraint to satisfy
        :return: Constraint
        """

        min_n_rcvs = float('inf')
        result = None

        # For every constraint
        for c in self.a:
            # Number of associated RCVs
            n_rcvs = len(self.a[c])

            # Check if there are fewer than the running minimum
            if n_rcvs < min_n_rcvs:

                # Update minimum and save constraint
                min_n_rcvs = n_rcvs
                result = c

                # 1 is the minimum number of RCVs, so the first one we find will do.
                if n_rcvs == 1:
                    break

        return result

    def is_goal(self):
        """
        Is this state a goal?
        :return: True if this state is a goal
        """
        # A goal state will have no constraints left to fulfill in matrix A
        return all(item is None for item in self.a)

    def apply_solution(self):
        """
        Blindly apply the solution set to the initial values
        :return: updated values array
        """
        # Get RCV from solutions, and apply to grid.
        for y, x in self.solution.keys():
            self.values[y, x] = self.solution[y, x]

        return self.values
