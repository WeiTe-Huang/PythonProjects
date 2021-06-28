"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    length = width - GRAPH_MARGIN_SIZE * 2
    x_coordinate = GRAPH_MARGIN_SIZE + (length / len(YEARS) * year_index)
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')  # delete all existing lines from the canvas

    # Write your code below this line
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,
                       CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
                       CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE)
    for i in range(len(YEARS)):
        canvas.create_line(get_x_coordinate(CANVAS_WIDTH, i), 0,
                           get_x_coordinate(CANVAS_WIDTH, i), CANVAS_HEIGHT)
        canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i) + TEXT_DX,
                           CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, text=YEARS[i], anchor=tkinter.NW)
    canvas.create_line(get_x_coordinate(CANVAS_WIDTH, len(YEARS)), 0,
                       get_x_coordinate(CANVAS_WIDTH, len(YEARS)), CANVAS_HEIGHT)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)  # draw the fixed background grid
    # Write your code below this line
    for i in range(len(lookup_names)):
        while True:
            if i < len(YEARS):
                break
            i -= len(YEARS)
        color = COLORS[i]
        last_point_x = 0
        last_point_y = 0
        y_range = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE * 2
        for j in range(len(YEARS)):
            if j == 0:
                last_point_x = get_x_coordinate(CANVAS_WIDTH, j)
                if str(YEARS[j]) in name_data[lookup_names[i]]:

                    print(int(name_data[lookup_names[i]][str(YEARS[j])]))

                    last_point_y = GRAPH_MARGIN_SIZE + y_range / 1000 * int(name_data[lookup_names[i]][str(YEARS[j])])
                    canvas.create_text(last_point_x + TEXT_DX, last_point_y,
                                       text=lookup_names[i] + ' ' + name_data[lookup_names[i]][str(YEARS[j])],
                                       anchor=tkinter.SW, fill=color)
                else:
                    last_point_y = GRAPH_MARGIN_SIZE + y_range
                    canvas.create_text(last_point_x + TEXT_DX, last_point_y, text=lookup_names[i] + ' *',
                                       anchor=tkinter.SW, fill=color)
            else:
                this_point_x = get_x_coordinate(CANVAS_WIDTH, j)
                if str(YEARS[j]) in name_data[lookup_names[i]]:
                    this_point_y = GRAPH_MARGIN_SIZE + y_range / 1000 * int(name_data[lookup_names[i]][str(YEARS[j])])
                    canvas.create_text(this_point_x + TEXT_DX, this_point_y,
                                       text=lookup_names[i] + ' ' +name_data[lookup_names[i]][str(YEARS[j])],
                                       anchor=tkinter.SW, fill=color)
                else:
                    this_point_y = GRAPH_MARGIN_SIZE + y_range
                    canvas.create_text(this_point_x + TEXT_DX, this_point_y, text=lookup_names[i] + ' *',
                                       anchor=tkinter.SW, fill=color)
                canvas.create_line(last_point_x, last_point_y, this_point_x, this_point_y,
                                   width=LINE_WIDTH, fill=color)
                last_point_x = this_point_x
                last_point_y = this_point_y


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
