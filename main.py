"""
Tkinter window for running and displaying the snake game.
"""

import tkinter as tk
from configuration import Configuration
from game import Game
from draw import Draw


class Combined(tk.Tk):
    """
    Tkinter window for running and displaying the snake game. This class
    creates the main window, controls, and canvas.

    Attributes
    ----------
    config_obj : Configuration
        The Configuration object.
    game_obj : Game
        The Game object.
    draw_obj : Draw
        The Draw object.
    next_step_call : str | None
        tracker for game loop callback.
    paused : boolean
        True if the game is currently paused.
    score_label : tk.Label
        Label showing current score.
    status : tk.Label
        Label showing game status.
    obstacles_on : tk.BooleanVar
        Obstacles enabled boolean.
    wrap_on : tk.BooleanVar
        Wrap walls enabled boolean.
    invincible_on : tk.BooleanVar
        Invincibility enabled boolean.
    canvas : tk.Canvas
        Canvas where the game is drawn.

    Methods
    -------
    toggle_pause()
        Toggle the paused state of the game.
    start_game()
        Start or reset the game and begin the main loop.
    game_loop()
        Main recurring callback that advances and redraws the game.
    """

    def __init__(self):
        """
        Initialize the window and widgets with title, score, toggles,
        status, and view.

        Returns
        -------
        None
        """
        tk.Tk.__init__(self)
        self.title("Snake Game")

        # Initial game configuration passed from configuration object
        self.config_obj = Configuration()
        self.next_step_call = None
        self.paused = False

        # Top bar with toggles/ controls
        top = tk.Frame(self)
        top.pack(side=tk.TOP, fill=tk.X)

        self.score_label = tk.Label(top, text="Score: 0", font=("Arial", 15))
        self.score_label.pack()

        self.status = tk.Label(top, text="Press Start / Reset", font=("Arial", 15))
        self.status.pack()

        # Controls
        controls = tk.Frame(self)
        controls.pack(side=tk.TOP, fill=tk.X)

        self.obstacles_on = tk.BooleanVar(value=True)
        tk.Checkbutton(
            controls,
            text="Obstacle blobs",
            variable=self.obstacles_on,
            font=("Arial", 15),
        ).pack()

        self.wrap_on = tk.BooleanVar(value=False)
        tk.Checkbutton(
            controls,
            text="Wrap walls",
            variable=self.wrap_on,
            font=("Arial", 15),
        ).pack()

        self.invincible_on = tk.BooleanVar(value=False)
        tk.Checkbutton(
            controls,
            text="Invincible",
            variable=self.invincible_on,
            font=("Arial", 15),
        ).pack()

        tk.Button(
            controls,
            text="Start / Reset",
            command=self.start_game,
            font=("Arial", 15),
        ).pack()
        tk.Button(
            controls,
            text="Pause / Resume",
            command=self.toggle_pause,
            font=("Arial", 15),
        ).pack()

        # Canvas (sized based on cell size and grid size)
        self.canvas = tk.Canvas(
            self,
            width=self.config_obj.grid_width * self.config_obj.cell_size,
            height=self.config_obj.grid_height * self.config_obj.cell_size,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)

        # initial game view
        self.game_obj = Game(
            self.config_obj,
            obstacles_enabled=self.obstacles_on.get(),
            wrap_walls=self.wrap_on.get(),
            invincible=self.invincible_on.get(),
        )
        self.draw_obj = Draw(self.canvas, self.game_obj)

        # keyboard interface
        self.bind("<Up>", lambda e: self.game_obj.change_direction("Up"))
        self.bind("<Down>", lambda e: self.game_obj.change_direction("Down"))
        self.bind("<Left>", lambda e: self.game_obj.change_direction("Left"))
        self.bind("<Right>", lambda e: self.game_obj.change_direction("Right"))
        self.bind("<space>", lambda e: self.toggle_pause())

    def toggle_pause(self):
        """
        Pause/ unpause game.

        Returns
        -------
        None
        """
        if self.game_obj.game_over:
            return
        self.paused = not self.paused
        if self.paused:
            self.status.config(text="Paused")
        else:
            self.status.config(text="Running")

    def start_game(self):
        """
        Starts a new game. Cancels any existing game loop, creates a new
        Game and GUI and starts the main loop.

        Returns
        -------
        None
        """
        # Cancel any previously scheduled game-loop callback
        if self.next_step_call:
            self.after_cancel(self.next_step_call)
            self.next_step_call = None

        self.paused = False

        # New game drawing
        self.game_obj = Game(
            self.config_obj,
            obstacles_enabled=self.obstacles_on.get(),
            wrap_walls=self.wrap_on.get(),
            invincible=self.invincible_on.get(),
        )
        self.draw_obj = Draw(self.canvas, self.game_obj)

        self.status.config(text="Running")
        self.score_label.config(text=f"Score: {self.game_obj.score} ")
        self.draw_obj.draw()

        # Continue game_obj
        self.game_loop()

    def game_loop(self):
        """
        Advances the game by a step, redraws the view, updates score, and
        sets to run again after the configured delay.

        Returns
        -------
        None
        """
        if not self.paused:
            self.game_obj.step()

        self.draw_obj.draw()
        self.score_label.config(text=f"Score: {self.game_obj.score} ")

        if self.game_obj.game_over:
            self.status.config(text="Game over")
            self.next_step_call = None
            return

        # Schedule the next game tick after the configured delay
        self.next_step_call = self.after(
            self.config_obj.step_delay,
            self.game_loop,
        )


if __name__ == "__main__":
    Combined().mainloop()