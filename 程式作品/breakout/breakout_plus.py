"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gobjects import GRect, GOval, GLabel
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked
from breakout_plus_data import Breakout, Starter, BreakOutColor


FRAME_RATE = 1000 / 60   # 60 frames per second
NUM_LIVES = 3		 # Number of attempts

# Starter
start = Starter()
style = ''
level = ''
size = ''

# Red select button1
red_select1 = GRect(start.classic_button.width - 12, start.classic_button.height - 12)
red_select1.color = 'red'
red_select1.filled = True
red_select1.fill_color = red_select1.color
start.window.add(red_select1, start.window.width, start.window.height)
rs1 = False

# Red select button2
red_select2 = GRect(start.classic_button.width + 5, start.classic_button.height + 5)
red_select2.color = 'red'
start.window.add(red_select2, start.window.width, start.window.height)
rs2 = False

# Red select button3
red_select3 = GOval(10, 10)
red_select3.color = 'red'
red_select3.filled = True
red_select3.fill_color = red_select1.color
start.window.add(red_select3, start.window.width, start.window.height)
rs3 = False

def main():
    onmouseclicked(choose)


def breakout_graphic(stylish, difficulty, sizer):
    if difficulty == 'easy':
        width = 100
    elif difficulty == 'medium':
        width = 80
    else:
        width = 60

    if sizer == 'small':
        number = 7
    elif sizer == 'medium':
        number = 10
    else:
        number = 13

    lives = NUM_LIVES
    score = 0

    breakout = Breakout(style=stylish, paddle_width=width, brick_cols=number, brick_rows=number)
    scoreboard = GLabel('Score: ' + str(score))
    scoreboard.color = BreakOutColor(stylish).ball_color
    scoreboard.font = 'Courier-15'
    breakout.window.add(scoreboard, 5, breakout.brick_offset / 2 + scoreboard.height / 2)

    liveboard = GLabel('Lives: ' + '♥ ' * lives)
    liveboard.color = BreakOutColor(stylish).ball_color
    liveboard.font = 'Courier-15'
    breakout.window.add(liveboard, breakout.window.width - 89 - 24 * NUM_LIVES, breakout.brick_offset / 2 + scoreboard.height / 2)

    dx = breakout.get_dx()
    if difficulty == 'easy':
        dy = breakout.get_dy() - 2
    elif difficulty == 'medium':
        dy = breakout.get_dy()
    else:
        dy = breakout.get_dy() + 2
    if sizer == 'small':
        dy -= 2
    elif sizer == 'medium':
        pass
    else:
        dy += 1

    bricks = breakout.bricks

    while True:
        if breakout.start is True:
            breakout.ball.move(dx, dy)
            if breakout.ball.x > breakout.window.width - breakout.ball.width or breakout.ball.x < 0:
                dx *= -1
                breakout.ball.move(dx, dy)
            if breakout.ball.y < 0:
                dy *= -1
                breakout.ball.move(dx, dy)
            if breakout.ball.y > breakout.window.height - breakout.ball.height:
                breakout.start = False
                breakout.window.remove(liveboard)
                lives -= 1
                liveboard = GLabel('Lives: ' + '♥ ' * lives)
                liveboard.color = BreakOutColor(stylish).ball_color
                liveboard.font = 'Courier-15'
                breakout.window.add(liveboard, breakout.window.width - 89 - 24 * NUM_LIVES, breakout.brick_offset / 2 + scoreboard.height / 2)
                if lives == 0:
                    breakout.game_over()

                    break
                breakout.ball.x = (breakout.window.width - breakout.ball.width) / 2
                breakout.ball.y = (breakout.window.height - breakout.ball.height) / 2
            if breakout.touch() is not None and breakout.touch() is not scoreboard:
                if breakout.touch() == breakout.paddle:
                    dy *= -1
                    breakout.ball.y = breakout.paddle.y - breakout.ball.height
                else:
                    if breakout.touch() != breakout.background:
                        dy *= -1
                        if breakout.touch().color == breakout.touch().fill_color:
                            breakout.touch().fill_color = BreakOutColor(breakout.style).background_color
                        else:
                            breakout.window.remove(breakout.touch())
                            bricks -= 1
                            breakout.window.remove(scoreboard)
                            score += 1
                            scoreboard = GLabel('Score: ' + str(score))
                            scoreboard.color = BreakOutColor(stylish).ball_color
                            scoreboard.font = 'Courier-15'
                            breakout.window.add(scoreboard, 5, breakout.brick_offset / 2 + scoreboard.height / 2)
                        if bricks == 0:
                            breakout.you_win()
                            break
        pause(FRAME_RATE)

def choose(click):
    global style, rs1, level, rs2, size, rs3
    if start.window.get_object_at(click.x, click.y) == start.classic_button:
        style = 'classic'
        red_select1.location = start.classic_button.x + 6, start.classic_button.y + 6
        rs1 = True
        if rs1 is True and rs2 is True and rs3 is True:
            start.window.add(start.start_game_rect, (start.window.width - start.start_game_rect.width) / 2, 455)
            start.window.add(start.start_game_shadow, (start.window.width - start.start_game_shadow.width) / 2 + 3, 518)
            start.window.add(start.start_game, (start.window.width - start.start_game.width) / 2, 515)
    if start.window.get_object_at(click.x, click.y) == start.neon_button:
        style = 'neon'
        red_select1.location = start.neon_button.x + 6, start.neon_button.y + 6
        rs1 = True
        if rs1 is True and rs2 is True and rs3 is True:
            start.window.add(start.start_game_rect, (start.window.width - start.start_game_rect.width) / 2, 455)
            start.window.add(start.start_game_shadow, (start.window.width - start.start_game_shadow.width) / 2 + 3, 518)
            start.window.add(start.start_game, (start.window.width - start.start_game.width) / 2, 515)
    if start.window.get_object_at(click.x, click.y) == start.forest_button:
        style = 'forest'
        red_select1.location = start.forest_button.x + 6, start.forest_button.y + 6
        rs1 = True
        if rs1 is True and rs2 is True and rs3 is True:
            start.window.add(start.start_game_rect, (start.window.width - start.start_game_rect.width) / 2, 455)
            start.window.add(start.start_game_shadow, (start.window.width - start.start_game_shadow.width) / 2 + 3, 518)
            start.window.add(start.start_game, (start.window.width - start.start_game.width) / 2, 515)

    if start.window.get_object_at(click.x, click.y) == start.easy_button:
        level = 'easy'
        red_select2.location = start.easy_button.x - 1, start.easy_button.y - start.easy_button.height - 7
        rs2 = True
        if rs1 is True and rs2 is True and rs3 is True:
            start.window.add(start.start_game_rect, (start.window.width - start.start_game_rect.width) / 2, 455)
            start.window.add(start.start_game_shadow, (start.window.width - start.start_game_shadow.width) / 2 + 3, 518)
            start.window.add(start.start_game, (start.window.width - start.start_game.width) / 2, 515)
    if start.window.get_object_at(click.x, click.y) == start.normal_button:
        level = 'medium'
        red_select2.location = start.normal_button.x - 1, start.normal_button.y - start.normal_button.height - 7
        rs2 = True
        if rs1 is True and rs2 is True and rs3 is True:
            start.window.add(start.start_game_rect, (start.window.width - start.start_game_rect.width) / 2, 455)
            start.window.add(start.start_game_shadow, (start.window.width - start.start_game_shadow.width) / 2 + 3, 518)
            start.window.add(start.start_game, (start.window.width - start.start_game.width) / 2, 515)
    if start.window.get_object_at(click.x, click.y) == start.hard_button:
        level = 'large'
        red_select2.location = start.hard_button.x - 1, start.hard_button.y - start.hard_button.height - 7
        rs2 = True
        if rs1 is True and rs2 is True and rs3 is True:
            start.window.add(start.start_game_rect, (start.window.width - start.start_game_rect.width) / 2, 455)
            start.window.add(start.start_game_shadow, (start.window.width - start.start_game_shadow.width) / 2 + 3, 518)
            start.window.add(start.start_game, (start.window.width - start.start_game.width) / 2, 515)

    if start.window.get_object_at(click.x, click.y) == start.small_button:
        size = 'small'
        red_select3.location = start.small_button.x + start.small_button.width / 2 - 3, start.small_button.y + 3
        rs3 = True
        if rs1 is True and rs2 is True and rs3 is True:
            start.window.add(start.start_game_rect, (start.window.width - start.start_game_rect.width) / 2, 455)
            start.window.add(start.start_game_shadow, (start.window.width - start.start_game_shadow.width) / 2 + 3, 518)
            start.window.add(start.start_game, (start.window.width - start.start_game.width) / 2, 515)
    if start.window.get_object_at(click.x, click.y) == start.medium_button:
        size = 'medium'
        red_select3.location = start.medium_button.x + start.medium_button.width / 2 - 3, start.medium_button.y + 3
        rs3 = True
        if rs1 is True and rs2 is True and rs3 is True:
            start.window.add(start.start_game_rect, (start.window.width - start.start_game_rect.width) / 2, 455)
            start.window.add(start.start_game_shadow, (start.window.width - start.start_game_shadow.width) / 2 + 3, 518)
            start.window.add(start.start_game, (start.window.width - start.start_game.width) / 2, 515)
    if start.window.get_object_at(click.x, click.y) == start.large_button:
        size = 'large'
        red_select3.location = start.large_button.x + start.large_button.width / 2 - 3, start.large_button.y + 3
        rs3 = True
        if rs1 is True and rs2 is True and rs3 is True:
            start.window.add(start.start_game_rect, (start.window.width - start.start_game_rect.width) / 2, 455)
            start.window.add(start.start_game_shadow, (start.window.width - start.start_game_shadow.width) / 2 + 3, 518)
            start.window.add(start.start_game, (start.window.width - start.start_game.width) / 2, 515)

    if start.window.get_object_at(click.x, click.y) == start.start_game_rect \
            or start.window.get_object_at(click.x, click.y) == start.start_game_shadow \
            or start.window.get_object_at(click.x, click.y) == start.start_game:
        breakout_graphic(style, level, size)



if __name__ == '__main__':
    main()
