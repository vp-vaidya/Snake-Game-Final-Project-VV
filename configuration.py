"""
Configuration container for the snake game.
"""


class Configuration:
    """
    Configuration container for the snake game.

    Attributes
    ----------
    grid_width : int
        Number of columns in the grid.
    grid_height : int
        Number of rows in the grid.
    cell_size : int
        Pixel size of each cell.
    step_delay : int
        Millisecond delay between steps (can be used to adjust snake speed).
    powerup_chance : float
        Probability each step to generate a new power-up.
    obstacle_density : float
        Fraction of board cells targeted to become obstacle cells.
    """

    def __init__(
        self,
        grid_width=15,
        grid_height=15,
        cell_size=40,
        step_delay=150,
        powerup_chance=0.01,
        obstacle_density=0.2,
    ):
        """
        Set up the game configuration, default values incorporated.
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.step_delay = step_delay
        self.powerup_chance = powerup_chance
        self.obstacle_density = obstacle_density
