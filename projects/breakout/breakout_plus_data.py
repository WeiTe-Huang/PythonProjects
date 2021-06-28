"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gcolor import GColor
from campy.graphics.gwindow import GWindow
from campy.graphics.gimage import GImage
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 60  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 15  # Radius of the ball (in pixels).
PADDLE_WIDTH = 85  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.


class Breakout:
    def __init__(self, style, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):
        self.brick_offset = brick_offset

        # Style(color)
        self.style = style

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_rows * (brick_width + brick_spacing) + brick_offset * 3
        self.window = GWindow(width=window_width, height=window_height, title=title)
        self.background = GRect(window_width, window_height)
        self.background.color = BreakOutColor(style).background_color
        self.background.filled = True
        self.background.fill_color = self.background.color
        self.window.add(self.background)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.color = BreakOutColor(style).ball_color
        self.paddle.filled = True
        self.paddle.fill_color = self.paddle.color
        self.window.add(self.paddle, (self.window.width - self.paddle.width) / 2,
                        self.window.height - paddle_offset)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius, ball_radius)
        self.ball.color = BreakOutColor(style).ball_color
        self.ball.filled = True
        self.ball.fill_color = self.ball.color
        self.window.add(self.ball, (self.window.width - self.ball.width) / 2,
                        (self.window.height - self.ball.height) / 2)

        # Default initial velocity for the ball
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx *= -1
        self.__dy = INITIAL_Y_SPEED

        # Initialize mouse listeners
        onmouseclicked(self.start_game)
        onmousemoved(self.move_paddle)

        # Bricks
        for i in range(brick_cols):
            for j in range(brick_rows):
                self.brick = GRect(brick_width, brick_height)
                self.brick.line_width *= 2
                self.brick.filled = True
                if style == 'forest':
                    self.brick.color = GColor(BreakOutColor(style).brick_color_end.r +
                                              int(((BreakOutColor(style).brick_color_start.r -
                                                    BreakOutColor(style).brick_color_end.r) / brick_cols) * j),
                                              BreakOutColor(style).brick_color_start.g +
                                              int(((BreakOutColor(style).brick_color_start.g -
                                                    BreakOutColor(style).brick_color_end.g) / brick_cols) * j),
                                              BreakOutColor(style).brick_color_start.b +
                                              int(((BreakOutColor(style).brick_color_start.b -
                                                    BreakOutColor(style).brick_color_end.b) / brick_cols) * j))
                else:
                    self.brick.color = BreakOutColor(style).brick_color[
                        random.randint(0, len(BreakOutColor(style).brick_color) - 1)]
                self.brick.fill_color = self.background.color
                if random.random() < 0.3:
                    self.brick.fill_color = self.brick.color
                self.window.add(self.brick, (brick_width + brick_spacing) * i,
                                brick_offset + (brick_height + brick_spacing) * j)
        self.bricks = brick_cols * brick_rows

        # Game start button
        self.start_button = GLabel('GAME START')
        self.start_button.color = BreakOutColor(style).ball_color
        self.start_button.font = 'Courier-30'
        self.start_button_rect = GRect(self.start_button.width + 20, self.start_button.height + 20)
        self.start_button_rect.line_width = 7.0
        self.start_button_rect.filled = True
        self.start_button_rect.fill_color = BreakOutColor(style).background_color
        if style == 'forest':
            self.start_button_rect.color = BreakOutColor(style).brick_color_start
        else:
            self.start_button_rect.color = BreakOutColor(style).brick_color[random.randint(0, len(BreakOutColor(style).brick_color) - 1)]
        self.window.add(self.start_button_rect, (self.window.width - self.start_button_rect.width) / 2,
                        (self.window.height - self.start_button_rect.height) / 2 - 8)
        self.window.add(self.start_button, (self.window.width - self.start_button.width) / 2,
                        (self.window.height - self.start_button.height) / 2 + self.start_button.height)
        self.start = False

        # Leave button
        self.leave_button = GLabel('leave')
        self.leave_button.color = BreakOutColor(self.style).ball_color
        self.leave_button.font = 'Courier-15'

        self.leave_button_rect = GRect(self.leave_button.width + 10, self.leave_button.height + 10)
        self.leave_button_rect.color = 'red'
        self.leave_button_rect.filled = True
        self.leave_button_rect.fill_color = self.leave_button_rect.color

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def start_game(self, click):
        if self.window.get_object_at(click.x, click.y) == self.start_button or \
                self.window.get_object_at(click.x, click.y) == self.start_button_rect:
            self.window.remove(self.start_button)
            self.window.remove(self.start_button_rect)
            self.start = True
        elif self.window.get_object_at(self.window.width / 2, self.window.height / 2) is not self.start_button and \
                self.ball.x == (self.window.width - self.ball.width) / 2 and \
                self.ball.y == (self.window.height - self.ball.height) / 2:
            self.start = True
        if self.window.get_object_at(click.x, click.y) == self.leave_button or self.window.get_object_at(click.x, click.y) == self.leave_button_rect:
            self.window.close()
        return self.start

    def move_paddle(self, moved):
        if self.paddle.x > self.window.width - self.paddle.width:
            self.paddle.x = self.window.width - self.paddle.width
        elif self.paddle.x < 0:
            self.paddle.x = 0
        else:
            self.paddle.x = moved.x - self.paddle.width / 2

    def touch(self):
        point1 = self.window.get_object_at(self.ball.x, self.ball.y)
        point2 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        point3 = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)
        point4 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height)
        while True:
            if point1 is not None:
                return point1
            elif point2 is not None:
                return point2
            elif point3 is not None:
                return point3
            elif point4 is not None:
                return point4
            return None

    def game_over(self):
        game_over_background = GRect(self.window.width, self.window.height)
        game_over_background.color = BreakOutColor(self.style).background_color
        game_over_background.filled = True
        game_over_background.fill_color = game_over_background.color
        self.window.add(game_over_background)

        game_over_label = GLabel('GAME OVER')
        game_over_label.color = BreakOutColor(self.style).ball_color
        game_over_label.font = 'Courier-30'
        self.window.add(game_over_label, (self.window.width - game_over_label.width) / 2, (self.window.height - game_over_label.height) / 2)

        pause(900)
        self.window.add(self.leave_button_rect, (self.window.width - self.leave_button_rect.width) / 2,
                        (self.window.height - self.leave_button_rect.height) / 2 + game_over_label.height - self.leave_button.height - 6)
        self.window.add(self.leave_button, (self.window.width - self.leave_button.width) / 2,
                        (self.window.height - self.leave_button_rect.height) / 2 + game_over_label.height)

    def you_win(self):
        you_win_background = GRect(self.window.width, self.window.height)
        you_win_background.color = BreakOutColor(self.style).background_color
        you_win_background.filled = True
        you_win_background.fill_color = you_win_background.color
        self.window.add(you_win_background)

        you_win_label = GLabel('YOU WIN!')
        you_win_label.color = BreakOutColor(self.style).ball_color
        you_win_label.font = 'Courier-30'
        self.window.add(you_win_label, (self.window.width - you_win_label.width) / 2, (self.window.height - you_win_label.height) / 2)

        pause(900)
        self.window.add(self.leave_button_rect, (self.window.width - self.leave_button_rect.width) / 2,
                        (self.window.height - self.leave_button_rect.height) / 2 + you_win_label.height - self.leave_button.height - 6)
        self.window.add(self.leave_button, (self.window.width - self.leave_button.width) / 2,
                        (self.window.height - self.leave_button_rect.height) / 2 + you_win_label.height)


class BreakOutColor:
    def __init__(self, style='classic'):
        if style == 'neon':
            self.background_color = GColor(0, 0, 0)
            self.brick_color = [GColor(8, 247, 238), GColor(254, 83, 187),
                                GColor(245, 211, 0), GColor(113, 34, 250),
                                GColor(255, 148, 114), GColor(121, 255, 254)]
            self.bomb_color = GColor(255, 0, 0)
            self.bonus_color = GColor(255, 255, 0)
            self.ball_color = GColor(255, 255, 255)

        if style == 'classic':
            self.background_color = 'white'
            self.brick_color = ['red', 'orange', 'green', 'cyan', 'blue', 'purple']
            self.bomb_color = 'magenta'
            self.bonus_color = 'yellow'
            self.ball_color = 'black'

        if style == 'forest':
            self.background_color = GColor(255, 255, 255)
            self.brick_color_start = GColor(155, 97, 40)
            self.brick_color_end = GColor(58, 105, 79)
            self.bomb_color = GColor(255, 0, 0)
            self.bonus_color = GColor(255, 255, 0)
            self.ball_color = GColor(91, 73, 51)


class Starter:
    def __init__(self):

        # Window
        self.window = GWindow(800, 555, title='Starter')
        background = GRect(self.window.width, self.window.height)
        background.color = 'white'
        background.filled = True
        background.fill_color = background.color
        self.window.add(background)
        title = GImage('breakout_title.png')
        self.window.add(title, (self.window.width - title.width) / 2, 50)

        # # Select mode
        # select_mode = GLabel('Select Mode: ')
        # select_mode.font = 'Courier-20-bold'
        # select_mode.color = 'black'
        # self.window.add(select_mode, 70, 260)

        # breakout_button = GRect()
        # breakout_plus_button = GRect()

        # Select color
        select_color = GLabel('Select Color: ')
        select_color.font = 'Courier-20-bold'
        select_color.color = 'black'
        self.window.add(select_color, 70, 260)

        self.classic_button = GRect(select_color.height + 5, select_color.height + 5)
        self.classic_button.color = 'orange'
        self.classic_button.filled = True
        self.classic_button.fill_color = self.classic_button.color
        self.window.add(self.classic_button, 360, 230)

        self.neon_button = GRect(select_color.height + 5, select_color.height + 5)
        self.neon_button.color = GColor(121, 255, 254)
        self.neon_button.filled = True
        self.neon_button.fill_color = self.neon_button.color
        self.window.add(self.neon_button, 510, 230)

        self.forest_button = GRect(select_color.height + 5, select_color.height + 5)
        self.forest_button.color = GColor(58, 105, 79)
        self.forest_button.filled = True
        self.forest_button.fill_color = self.forest_button.color
        self.window.add(self.forest_button, 660, 230)

        # Select level
        select_level = GLabel('Select Level: ')
        select_level.font = 'Courier-20-bold'
        select_level.color = 'black'
        self.window.add(select_level, 70, 330)

        self.easy_button = GLabel('😀')
        self.easy_button.font = '-20-bold'
        self.easy_button.color = 'green'
        self.window.add(self.easy_button, 360, 330)

        self.normal_button = GLabel('😐')
        self.normal_button.font = '-20-bold'
        self.normal_button.color = 'orange'
        self.window.add(self.normal_button, 510, 330)

        self.hard_button = GLabel('😈')
        self.hard_button.font = '-20-bold'
        self.hard_button.color = 'red'
        self.window.add(self.hard_button, 660, 330)

        # Select size
        select_size = GLabel('Select Size: ')
        select_size.font = 'Courier-20-bold'
        select_size.color = 'black'
        self.window.add(select_size, 70, 400)

        self.small_button = GLabel('small')
        self.small_button.font = 'Courier-20'
        self.small_button.color = 'black'
        self.window.add(self.small_button, 360 - self.small_button.width / 2 + 16, 400)

        self.medium_button = GLabel('medium')
        self.medium_button.font = 'Courier-20'
        self.medium_button.color = 'black'
        self.window.add(self.medium_button, 510 - self.medium_button.width / 2 + 16, 400)

        self.large_button = GLabel('large')
        self.large_button.font = 'Courier-20'
        self.large_button.color = 'black'
        self.window.add(self.large_button, 660 - self.large_button.width / 2 + 16, 400)

        # Start Game
        self.start_game_rect_grey= GRect(320, 70)
        self.start_game_rect_grey.color = '#EBEBEB'
        self.start_game_rect_grey.filled = True
        self.start_game_rect_grey.fill_color = self.start_game_rect_grey.color
        self.window.add(self.start_game_rect_grey, (self.window.width - self.start_game_rect_grey.width) / 2, 455)

        self.start_game_shadow_grey= GLabel('START GAME')
        self.start_game_shadow_grey.font = 'Courier-35-bold'
        self.start_game_shadow_grey.color = '#CCCCCC'
        self.window.add(self.start_game_shadow_grey, (self.window.width - self.start_game_shadow_grey.width) / 2 + 3, 518)

        self.start_game_grey= GLabel('START GAME')
        self.start_game_grey.font= 'Courier-35-bold'
        self.start_game_grey.color= '#A3A3A3'
        self.window.add(self.start_game_grey, (self.window.width - self.start_game_grey.width) / 2, 515)

        self.start_game_rect = GRect(320, 70)
        self.start_game_rect.filled = True
        self.start_game_rect.fill_color = 'black'

        self.start_game_shadow = GLabel('START GAME')
        self.start_game_shadow.font = 'Courier-35-bold'
        self.start_game_shadow.color = 'red'

        self.start_game = GLabel('START GAME')
        self.start_game.font = 'Courier-35-bold'
        self.start_game.color = 'yellow'