"""
Drawing layer for the snake game using Tkinter.
"""


class Draw:
    """
    Drawing layer for the Snake game.

    Attributes
    ----------
    canvas : tk.Canvas
        The Tkinter canvas on which the game is drawn.
    game : Game
        The Game object tracking the game state for visualization.

    Methods
    -------
    draw_obstacles()
        Draw all obstacle cells.
    draw_food()
        Draw the food item, if present.
    draw_powerup()
        Draw the power-up item, if present.
    draw_snake()
        Draw the snake body and head.
    draw()
        Draw the entire game on the canvas.
    """

    def __init__(self, canvas, game):
        """
        Initialize a GUI.
        """
        self.canvas = canvas
        self.game = game

    def draw_obstacles(self):
        """
        Draw all obstacle cells as gray rectangles on the canvas.

        Returns
        -------
        None
        """
        for c in self.game.obstacles:
            x, y = c
            s = self.game.config.cell_size
            x1, y1, x2, y2 = x * s, y * s, x * s + s, y * s + s
            self.canvas.create_rectangle(
                x1, y1, x2, y2, fill="#666666", outline=""
            )

    def draw_food(self):
        """
        Draw the food as a red circle on the canvas

        Returns
        -------
        None
        """
        if self.game.food_position is None:
            return
        x, y = self.game.food_position
        s = self.game.config.cell_size
        x1, y1, x2, y2 = x * s, y * s, x * s + s, y * s + s
        self.canvas.create_oval(
            x1 + 6, y1 + 6, x2 - 6, y2 - 6, fill="#ff4d4d", outline=""
        )

    def draw_powerup(self):
        """
        Draw the power-up item as a smaller purple circle.

        Returns
        -------
        None
        """
        if self.game.powerup_position is None:
            return
        x, y = self.game.powerup_position
        s = self.game.config.cell_size
        x1, y1, x2, y2 = x * s, y * s, x * s + s, y * s + s
        self.canvas.create_oval(
            x1 + 10,
            y1 + 10,
            x2 - 10,
            y2 - 10,
            fill="#800080",
            outline="white",
            width=1,
        )
        self.canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text="2x",
            fill="black",
            font=("Arial", 8, "bold"),
        )

    def draw_snake(self):
        """
        Draw the snake as green circles. The head is slightly larger than body segments.

        Returns
        -------
        None
        """

        s = self.game.config.cell_size
        for i in range(len(self.game.snake)):
            x, y = self.game.snake[i]
            cx, cy = x * s + s / 2, y * s + s / 2

            # head is slightly larger
            if i == 0:
                r = s * 0.5
            else:
                r = s * 0.4
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r, fill="#00ff66", outline=""
            )

    def draw(self):
        """
        Clears the canvas, sets background, and then draws obstacles, food, power-ups, and the snake.

        Returns
        -------
        None
        """
        self.canvas.delete("all")
        self.canvas.configure(bg="black")
        if self.game.obstacles_enabled:
            self.draw_obstacles()
        self.draw_food()
        self.draw_powerup()
        self.draw_snake()
