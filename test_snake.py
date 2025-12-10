import unittest

from configuration import Configuration
from game import Game


class TestGame(unittest.TestCase):
    """
    Unit tests for the snake game
    """

    def setUp(self):
        """
        Create a model game before each test
        """
        self.config = Configuration(
            grid_width=15,
            grid_height=15,
            step_delay=200,
        )
        self.game = Game(self.config, obstacles_enabled=False)

    def test_snake_moves_right(self):
        """
        Snake moves in current direction
        """
        self.game.food_position = (0, 0)
        head_before = self.game.snake[0]
        self.game.step()
        self.game.step()
        self.game.step()
        head_after = self.game.snake[0]

        self.assertEqual(head_after, (head_before[0] + 3, head_before[1]))

    def test_eating_food_grows_snake(self):
        """
        Eating food increases snake length
        """
        head_x, head_y = self.game.snake[0]

        # Food directly in front of the snake
        self.game.food_position = (head_x + 1, head_y)
        initial_length = len(self.game.snake)

        # Step towards food
        self.game.step()

        self.assertEqual(len(self.game.snake), initial_length + 1)

    def test_direction_cannot_reverse(self):
        """
        Can't make 180 degree turns
        """
        self.game.direction = "Right"
        self.game.change_direction("Left")
        self.assertEqual(self.game.next_direction, "Right")

    def test_wrap_walls_enabled(self):
        """
        Snake wraps around edge when enabled
        """
        game = Game(self.config, obstacles_enabled=False, wrap_walls=True)

        # start snake at left wall
        game.snake = [(0, 7), (1, 7), (2, 7)]
        game.direction = "Left"
        game.next_direction = "Left"

        # Have snake move onto wall
        game.step()
        self.assertFalse(game.game_over)
        self.assertEqual(game.snake[0][0], self.config.grid_width - 1)

    def test_invincible_mode_bounces(self):
        """
        Snake bounces off walls in invincible mode
        """
        game = Game(self.config, obstacles_enabled=False, invincible=True)

        # Start snake at left wall
        game.snake = [(0, 7), (1, 7), (2, 7)]
        game.direction = "Left"
        game.next_direction = "Left"

        game.step()
        self.assertFalse(game.game_over) 
        self.assertEqual(game.direction, "Right")

    def test_obstacle_collision_ends_game(self):
        """
        Hitting obstacle ends game
        """
        game = Game(self.config, obstacles_enabled=True, invincible=False)
        game.snake = [(2, 7), (1, 7), (0, 7)]
        game.obstacles.add((3, 7))
        game.direction = "Right"
        game.next_direction = "Right"

        # Step onto obstacle block
        game.step()
        self.assertTrue(game.game_over)


if __name__ == "__main__":
    unittest.main(verbosity=2)
