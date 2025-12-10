"""
Main game logic for the snake game.
"""

import random


# Creating dictionary for easy lookup of direction and opposite directions
# for bouncing
DIR = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}
OPP_DIR = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}


class Game:
    """
    Main game logic. Tracks snake body, food, power-ups, obstacles, score,
    growth, and game-over. Uses a step method to take snake through each step
    along with next move one frame at a time.

    Attributes
    ----------
    config : Configuration
        Configuration object wrapper with board settings.
    obstacles_enabled : boolean
        Allows generation of obstacles consisting of randomly dispersed 2x2
        blocks with overlap allowed.
    wrap_walls : boolean
        Allows snake to wrap around walls and appear on other side if true.
    invincible : boolean
        Allows snake to overlap itself and collisions with walls/obstacles
        result in a 180 degree turn if true
    snake : list[tuple[int, int]]
        List of (x, y) cells making up the snake with head at first position.
    new_growth : int
        Number of segments the snake needs to grow (2 for power up, 1 for
        normal food)
    score : int
        Current score.
    game_over : boolean
        Marked true once there is a collision.
    food_position : tuple[int, int] | None
        Coordinates containing food, or None if no food.
    powerup_position : tuple[int, int] | None
        Coordinates containing a power-up, or None if no power-up.
    obstacles : set[tuple[int, int]]
        Set of cells that are occupied by obstacles.
    direction : str
        Current direction ("Up", "Down", "Left", "Right").
    next_direction : str
        Next snake direction input by player applied at next step.
    input_locked : boolean
        Locks direction changes until next step.

    Methods
    -------
    reset()
        Reset the game to its initial state and generate starting
        food/obstacles.
    is_inside(cell)
        Check whether a given cell is inside the board boundaries.
    change_direction(new_dir)
        Set new direction for the next step.
    random_empty_cell()
        Find a random valid cell for food or power-ups.
    generate_obstacles()
        Generate random 2x2 obstacle blocks on the board.
    step()
        Advance the game by one step.
    """

    def __init__(self, config, obstacles_enabled=True,
                 wrap_walls=False, invincible=False):
        """
        Initialize game state
        """
        self.config = config
        self.obstacles_enabled = obstacles_enabled
        self.wrap_walls = wrap_walls
        self.invincible = invincible
        self.food_position = None
        self.powerup_position = None
        self.obstacles = set()
        self.input_locked = False
        self.reset()

    def reset(self):
        """
        Reset the game to its starting configuration and snake state. Initial
        snake is 3 blocks long, starts at the center of the board and is
        moving to the right. Reset also adds obstacles if enabled and
        generates first food.

        Returns
        -------
        None
        """
        gw = self.config.grid_width
        gh = self.config.grid_height

        # Initialize snake in center of the board with 3 segments moving to
        # the right.
        x0 = gw // 2
        y0 = gh // 2
        self.snake = [(x0, y0), (x0 - 1, y0), (x0 - 2, y0)]
        self.direction = "Right"
        self.next_direction = "Right"

        # Initial snake growth, score and game state
        self.new_growth = 0
        self.score = 0
        self.game_over = False

        # Generate new set of obstacles if enabled
        if self.obstacles_enabled:
            self.generate_obstacles()

        # Initial food, No initial power-up
        self.food_position = self.random_empty_cell()
        self.powerup_position = None

    def is_inside(self, cell):
        """
        Check whether a given cell is inside the board boundaries.

        Parameters
        ----------
        cell : tuple[int, int]
            (x, y) cell coordinates.

        Returns
        -------
        boolean
            True if the cell is within the grid.
        """
        x, y = cell
        gw = self.config.grid_width
        gh = self.config.grid_height
        if 0 <= x < gw and 0 <= y < gh:
            return True
        else:
            return False

    def change_direction(self, new_dir):
        """
        Set new direction input by player to apply to next step. Allows 90
        degree turns only to the right or left.

        Parameters
        ----------
        new_dir : str
            ("Up", "Down", "Left", "Right").

        Returns
        -------
        None
        """
        if new_dir not in DIR:
            return
        if self.input_locked:
            return
        # If same direction as current direction, disregard
        if new_dir == self.direction:
            return
        # No 180 degree turns
        if OPP_DIR[new_dir] == self.direction:
            return

        self.next_direction = new_dir

        # lock new input until next step
        self.input_locked = True

    def random_empty_cell(self):
        """
        Chooses a cell at random for generating food or power-ups. Cells with
        obstacles or currently occupied by the snake are invalid. Additionally,
        the generated food/power-up will have a 1 cell radius around it empty.

        Returns
        -------
        tuple[int, int] or None
            A random empty cell satisfying the constraints, or None if no such
            cell exists.
        """

        # snake and obstacle cells are invalid
        occupied = set(self.snake)
        for cell in self.obstacles:
            occupied.add(cell)

        # food and power-up cells are invalid
        if self.food_position is not None:
            occupied.add(self.food_position)
        if self.powerup_position is not None:
            occupied.add(self.powerup_position)

        # initialize list of candidate cells.
        cells = []
        for x in range(self.config.grid_width-1):
            for y in range(self.config.grid_height-1):
                cell = (x, y)
                # check if cell is occupied
                if cell in occupied:
                    continue

                # Enforce 1-block radius empty around the cell
                valid = True
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        neighbor = (nx, ny)
                        if neighbor in occupied:
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    cells.append(cell)
        if len(cells) == 0:
            print("No valid cells found.")
            return None
        return random.choice(cells)

    def generate_obstacles(self):
        """
        Generate random 2×2 obstacle blocks on the board with overlap allowed.
        Each new game resets and generates new obstacles. Obstacles will not be
        generated in the first 6x3 cells in front of the snake to prevent
        immediate loss. Obstacles will be generated with a random placement
        of the lower left cell and then built out to be 2x2 cells.

        Returns
        -------
        None
        """
        # Clear any existing obstacles
        self.obstacles.clear()

        gw, gh = self.config.grid_width, self.config.grid_height
        total_cells = gw * gh
        obstacle_cells = int(total_cells * self.config.obstacle_density)

        block_number = obstacle_cells // 4

        # Starting snake cells are invalid for obstacles
        invalid_cells = set(self.snake)

        # First 6x3 cells in front of snake are invalid
        head_x = gw // 2
        head_y = gh // 2
        for i in range(1, 7):  # 1 to 6
            for j in (-1, 0, 1):
                nx = head_x + i
                ny = head_y + j
                invalid_cells.add((nx, ny))

        # randomly place obstacle blocks indexing by the bottom left block.
        for blocks in range(block_number):
            x = random.randint(0, gw - 2)
            y = random.randint(0, gh - 2)

            # build out rest of obstacle block
            block_cells = [
                (x, y),
                (x + 1, y),
                (x, y + 1),
                (x + 1, y + 1),
            ]

            # check if cells in the obstacle block are valid
            block_is_invalid = False
            for cell in block_cells:
                if cell in invalid_cells:
                    block_is_invalid = True
                    break
            if block_is_invalid:
                continue
            for cell in block_cells:
                self.obstacles.add(cell)

    def step(self):
        """
        Advances the game by one step. Applies next direction input by player.
        Computes new snake cell positions taking into account player input and
        toggle settings (collisions, wall wrap, etc). Adds any new food or
        power-ups to score and grows the snake accordingly. For snake movement
        with each step, The tail position is removed and a new head position
        is added. step also generates a new power up based on probability
        setting.

        Returns
        -------
        None
        """
        if self.game_over:
            return

        # Allow one turn per step
        self.input_locked = False
        self.direction = self.next_direction

        # New head position
        gw, gh = self.config.grid_width, self.config.grid_height
        head = self.snake[0]
        dx, dy = DIR[self.direction]
        nx, ny = head[0] + dx, head[1] + dy

        # Walls
        if self.wrap_walls:
            nx = nx % gw
            ny = ny % gh
            new_head = (nx, ny)
        else:
            new_head = (nx, ny)
            # If snake hits a wall
            if not self.is_inside(new_head):
                if self.invincible:
                    # bounce
                    bounce_dir = OPP_DIR[self.direction]
                    bdx, bdy = DIR[bounce_dir]
                    bx, by = head[0] + bdx, head[1] + bdy
                    bounce_cell = (bx, by)
                    if self.is_inside(bounce_cell):
                        self.direction = bounce_dir
                        self.next_direction = bounce_dir
                        new_head = bounce_cell
                    else:
                        return
                else:
                    self.game_over = True
                    return

        # If snake hits an obstacle
        if new_head in self.obstacles:
            if self.invincible:
                bounce_dir = OPP_DIR[self.direction]
                bdx, bdy = DIR[bounce_dir]
                bx, by = head[0] + bdx, head[1] + bdy
                if self.wrap_walls:
                    bx = bx % gw
                    by = by % gh
                bounce_cell = (bx, by)
                if (self.is_inside(bounce_cell)
                        and bounce_cell not in self.obstacles):
                    self.direction = bounce_dir
                    self.next_direction = bounce_dir
                    new_head = bounce_cell
            else:
                self.game_over = True
                return

        # If snake hits itself
        if new_head in self.snake:
            if not self.invincible:
                self.game_over = True
                return

        # Move snake head
        self.snake.insert(0, new_head)

        # If snake hits food
        growth = 0
        if new_head == self.food_position:
            self.score = self.score + 1
            growth = growth + 1
            # generate new food
            self.food_position = self.random_empty_cell()

        # If snake hits power-up
        if new_head == self.powerup_position:
            self.score = self.score + 2
            growth = growth + 2
            # remove power up
            self.powerup_position = None

        # Add any new growth from this step
        self.new_growth = self.new_growth + growth

        if self.new_growth > 0:
            # Account for forward movement by snake every step and subtract 1
            # from any growth
            self.new_growth = self.new_growth - 1
        else:
            self.snake.pop()

        # Generate a new power-up based on probability
        if (self.powerup_position is None
                and random.random() < self.config.powerup_chance):
            self.powerup_position = self.random_empty_cell()
