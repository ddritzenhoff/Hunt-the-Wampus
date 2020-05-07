import curses
from random import randint, choice

class Info:
    # This class is full of static variables hence the case.
    BAT = "| B |"
    WAMPUS = "| W |"
    HERO = "| H |"
    UNDISCOVERED = "| ? |"
    DISCOVERED = "|   |"
    ROW_LENGTH = 5
    COLUMN_LENGTH = 5
    TOTAL_LENGTH = ROW_LENGTH * COLUMN_LENGTH
    up_direction = -ROW_LENGTH
    down_direction = ROW_LENGTH
    left_direction = -1
    right_direction = 1
    BAT_WARNING = "Bats nearby.\n"
    WUMPUS_WARNING = "I smell a Wampus.\n"
    PIT_WARNING = "I feel a draft.\n"
    QUIT_STATEMENT = "Press q to quit"
    menu = ['Play Game', 'Rules', 'Leave']
    _INSTRUCTIONS = """Welcome to 'Hunt the Wumpus'.
The Wumpus lives in a cave of 25 rooms. Each room has three or four paths leading
to other rooms.
Hazards:
Bottomless Pits: One room has a pit in it, and if you go there you
will fall, die, and lose.
Super Bats: One room has a super bat. If you go there, the bat will grab
you and take you to a random room. This could kill you!.
Wumpus: The Wumpus is not bothered by hazards as he has sucker feet and is
too big for a bat to lift. Usually he is asleep, but if you shoot him
or walk into his room he will wake up. When he wakes up, you die.
Turns: On each turn you may move or shoot a crooked arrow.
Move: You can move to an adjoining room through a path.
Shoot: You have five arrows to shoot (you run out you lose). Each arrow can
move through one room, and you aim by telling the computer which
direction to shoot. 
If the arrow hits the Wumpus you win.
Warnings: If you are one room from the Wumpus or a Hazard then you will see:
Wumpus: I smell a Wumpus.
Bat: Bats nearby.
Pit: I feel a draft.
"""
    Instructions = str.splitlines(_INSTRUCTIONS)

class Game:
    def __init__(self):

        self.explored_positions = []
        self.possible_positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        self.hero_pos = self.possible_positions[randint(0, len(self.possible_positions)-1)]
        self.possible_positions.remove(self.hero_pos)
        self.bat_1_pos = self.possible_positions[randint(0, len(self.possible_positions)-1)]
        self.possible_positions.remove(self.bat_1_pos)
        self.pit_1_pos = self.possible_positions[randint(0, len(self.possible_positions)-1)]
        self.possible_positions.remove(self.pit_1_pos)
        self.wampus_pos = self.possible_positions[randint(0, len(self.possible_positions)-1)]

        self.game_over = False
        self.arrows = 5
        self.explored_positions.append(self.hero_pos)
        self.reason_for_game_end = "no reason of death. This should not be here"
        self.dead_wampus = False
        
        hero_2d_pos = Pos(self.hero_pos)
        bat_1_2d_pos = Pos(self.bat_1_pos)
        pit_1_2d_pos = Pos(self.pit_1_pos)
        wampus_2d_pos = Pos(self.wampus_pos)

        print("Hero position is:", self.hero_pos, "or [", hero_2d_pos.row, ",", hero_2d_pos.column, "]")
        print("Bat 1 position is:", self.bat_1_pos, "or [", bat_1_2d_pos.row, ",", bat_1_2d_pos.column, "]")
        print("Pit 1 position is:", self.pit_1_pos, "or [", pit_1_2d_pos.row, ",", pit_1_2d_pos.column, "]")
        print("Wampus position is:", self.wampus_pos, "or [", wampus_2d_pos.row, ",", wampus_2d_pos.column, "]")

    # sound_warnings : [List-of Nat] -> Print statements
    # Sounds the warnings based on who the neighbors of the hero are.
    def sound_warnings(self, neighbors):
        warnings = []
        positions = {
            self.bat_1_pos: Info.BAT_WARNING, 
            self.pit_1_pos: Info.PIT_WARNING,
            self.wampus_pos: Info.WUMPUS_WARNING
            }
        [warnings.append(positions.get(neighbor)) for neighbor in neighbors if positions.get(neighbor, "nothing") != "nothing"]
        warnings = list(dict.fromkeys(warnings))
        return warnings

    # update_positions : Game Nat -> ???
    # Updates the hero position and the explored positions list 
    def update_positions(self, new_position):
        self.hero_pos = new_position
        self.explored_positions.append(self.hero_pos)
        self.explored_positions = list(dict.fromkeys(self.explored_positions))
        self.explored_positions.sort()
        if self.hero_pos == self.bat_1_pos:
            print("\nBats carried you away!")
            change_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
            change_list.remove(self.hero_pos)
            self.update_positions(choice(change_list))
        elif self.hero_pos == self.pit_1_pos:
            self.reason_for_game_end = "You have fallen into the pit... Game over!"
            self.game_over = True
        elif self.hero_pos == self.wampus_pos:
            self.reason_for_game_end = "You have been eaten by the wampus... Game over!"
            self.game_over = True

    # is_new_pos_valid : String -> Boolean
    # Determines if the input direction is a valid step
    def is_new_pos_valid(self, direction_value):
        new_dir = direction_value + self.hero_pos
        old_pos = Pos(self.hero_pos)
        new_pos = Pos(new_dir)
        return new_dir < Info.TOTAL_LENGTH and new_dir >= 0 and (old_pos.row == new_pos.row or old_pos.column == new_pos.column)
    # check_wampus_state : Game Nat -> None
    # Checks to see if the wampus is dead.
    def check_wampus_state(self, key_pressed):
        arrow_dict = {
            ord('w'): Info.up_direction,
            ord('s'): Info.down_direction,
            ord('a'): Info.left_direction,
            ord('d'): Info.right_direction
        }
        arrow_position = self.hero_pos + arrow_dict[key_pressed]
        if arrow_position == self.wampus_pos:
            self.game_over = True
            self.dead_wampus = True
            self.reason_for_game_end = "You have slain the wampus. You won!"

    # check_arrow_depletion_state : Game -> None
    # Checks to see if the arrows are depleted. 
    def check_arrow_depletion_state(self):
        if self.arrows <= 0:
            self.game_over = True
            self.reason_for_game_end = "You have run out of arrows... Game over."


class Pos:
    def __init__(self, num):
        self.row = int(num/Info.ROW_LENGTH)
        self.column = num % Info.ROW_LENGTH

# print_map : Nat [List-of Nat]-> [List-of String]
# Creates a list of strings that can be parsed and displayed
def print_map(hero_pos, _discovered):
    finished_array = []
    discovered = _discovered
    counter = 0
    for i in range(5):
        row = ""
        for j in range(5):
            if len(discovered) > 0 and counter == discovered[0]:
                if counter == hero_pos:
                    row+=Info.HERO
                else:
                    row+=Info.DISCOVERED
                discovered = discovered[1:]
            else:
                row+=Info.UNDISCOVERED
            counter+=1
        finished_array.append(row)
    return finished_array

# coords_to_pos : Nat Nat -> Nat
# Turns a 2d position into a 1D position.
def coords_to_pos(row, col):
    return Info.ROW_LENGTH*row + col

# get_neighbors : Number -> [List-of Number]
# Gets the neighboring indexes of the hero as a list of indexes
def get_neighbors(hero_pos):
    hero_coord = Pos(hero_pos)
    hero_row = hero_coord.row
    hero_col = hero_coord.column
    row_low_range = hero_row-1
    row_high_range = hero_row+2
    col_low_range = hero_col-1
    col_high_range = hero_col+2
    neighbors = []
    for i in range(row_low_range, row_high_range):
        for j in range(col_low_range, col_high_range):
            if i >= Info.ROW_LENGTH or i < 0 or j >= Info.COLUMN_LENGTH or j < 0 or i == hero_row and j == hero_col:
                pass
            else:
                neighbors.append(coords_to_pos(i, j))
    return neighbors

def main(stdscr):

    # To be later cleaned up.
    key_pressed = 0

    # To be later added to the INFO class.
    STATUSBARSTR = "Press W, S, A, and D keys to shoot and UP, DOWN, LEFT, and RIGHT arrow keys to move."
    UP_DOWN_LEFT_RIGHT_KEYS_PART_1 = "[^]"
    UP_DOWN_LEFT_RIGHT_KEYS_PART_2 = "[<][D][>]"
    W_S_A_D_KEYS_PART_1 = "[W]"
    W_S_A_D_KEYS_PART_2 = "[A][S][D]"

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    # make the cursor disappear.
    curses.curs_set(0)

    # Starting the game
    game = Game()

    while key_pressed != ord('q'):

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Render status bar
        status_bar_buffer = int((width - len(STATUSBARSTR)) // 2)
        stdscr.attron(curses.color_pair(3))
        move_amount = 0
        stdscr.addstr(0, move_amount, " " * status_bar_buffer)
        move_amount += status_bar_buffer
        stdscr.addstr(0, move_amount, STATUSBARSTR)
        move_amount += len(STATUSBARSTR)
        stdscr.addstr(0, move_amount, " " * (width - move_amount))
        stdscr.attroff(curses.color_pair(3))

        # Render keys below status bar
        box_size = len(W_S_A_D_KEYS_PART_1)
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(1, box_size, W_S_A_D_KEYS_PART_1)
        stdscr.addstr(1, width - len(UP_DOWN_LEFT_RIGHT_KEYS_PART_1) - box_size, UP_DOWN_LEFT_RIGHT_KEYS_PART_1)
        stdscr.addstr(2, 0, W_S_A_D_KEYS_PART_2)
        stdscr.addstr(2, width - len(UP_DOWN_LEFT_RIGHT_KEYS_PART_2), UP_DOWN_LEFT_RIGHT_KEYS_PART_2)
        stdscr.attroff(curses.color_pair(4))

        if game.game_over == True:
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(int(height // 2), int(width // 2 - len(game.reason_for_game_end) // 2 - len(game.reason_for_game_end) % 2), game.reason_for_game_end)
            stdscr.addstr(int(height // 2) + 4, int(width // 2 - len(Info.QUIT_STATEMENT) // 2 - len(Info.QUIT_STATEMENT) % 2), Info.QUIT_STATEMENT)
            stdscr.attroff(curses.color_pair(4))
            stdscr.refresh()
            key_pressed = stdscr.getch()
        else:   
            # Printing the map
            stdscr.attron(curses.color_pair(4))
            assembly = print_map(game.hero_pos, game.explored_positions)
            map_width = int(width // 2 - len(assembly[0]) // 2 - len(assembly[0]) % 2)
            for i in range(Info.ROW_LENGTH):
                stdscr.addstr(int(height // 2 - len(assembly) // 2 + i), int(width // 2 - len(assembly[i]) // 2 - len(assembly[i]) % 2), assembly[i])
            stdscr.attroff(curses.color_pair(4))

            # Printing the warnings
            stdscr.attron(curses.color_pair(1))
            neighbors = get_neighbors(game.hero_pos)
            warnings = game.sound_warnings(neighbors)
            for i in range(len(warnings)):
                stdscr.addstr(int(height // 2 - len(assembly) // 2 + i + len(assembly) + 1), int(width // 2 - len(warnings[i]) // 2 - len(warnings[i]) % 2), warnings[i])
            stdscr.attroff(curses.color_pair(1))

            # Printing the remaining arrows
            stdscr.attron(curses.color_pair(4))
            arrows_remaining = str(game.arrows) + " arrows remain."
            stdscr.addstr(height-1, int(width // 2 - len(arrows_remaining) // 2 - len(arrows_remaining) % 2), arrows_remaining)
            stdscr.attroff(curses.color_pair(4))

            # Refreshing the new contents onto the screen.
            stdscr.refresh()

            # Wait for next input
            key_pressed = stdscr.getch()

            # Interpreting inputs
            direction_value = 0
            if key_pressed == curses.KEY_UP:
                direction_value = Info.up_direction
            elif key_pressed == curses.KEY_DOWN:
                direction_value = Info.down_direction
            elif key_pressed == curses.KEY_RIGHT:
                direction_value = Info.right_direction
            elif key_pressed == curses.KEY_LEFT:
                direction_value = Info.left_direction
            elif key_pressed == ord('w') or key_pressed == ord('a') or key_pressed == ord('s') or key_pressed == ord('d'):
                game.arrows -= 1
                game.check_wampus_state(key_pressed)
                game.check_arrow_depletion_state()
            if direction_value != 0 and game.is_new_pos_valid(direction_value):
                new_pos = game.hero_pos + direction_value
                game.update_positions(new_pos)

def print_menu(stdscr, selected_row_id):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    for count, menu_item in enumerate(Info.menu):
        x_pos = width//2 - len(menu_item)//2 - len(menu_item) % 2
        y_pos = height//2 - len(Info.menu)//2 + count
        if count == selected_row_id:
            stdscr.attron(curses.color_pair(6))
            stdscr.addstr(y_pos, x_pos, menu_item)
            stdscr.attroff(curses.color_pair(6))
        else:
            stdscr.addstr(y_pos, x_pos, menu_item)
    stdscr.refresh()

def show_rules(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    exit_statement = "Press 'q' to leave for the main menu"
    buffer_length = int((width - len(exit_statement)) // 2)
    end_buffer = width - buffer_length - len(exit_statement)
    start_end_buffer = buffer_length + len(exit_statement)
    stdscr.attron(curses.color_pair(6))
    stdscr.addstr(0, 0, " "*buffer_length)
    stdscr.addstr(0, buffer_length, exit_statement)
    stdscr.addstr(0, start_end_buffer, " "*end_buffer)
    stdscr.attroff(curses.color_pair(6))
    for counter, line in enumerate(Info.Instructions):
        x_pos = width // 2 - len(line)//2 - len(line) % 2
        y_pos = height // 2 - len(Info.Instructions)//2 + counter
        stdscr.addstr(y_pos, x_pos, line)
    stdscr.refresh()
    exit_menu = False
    while exit_menu == False:
        key_pressed = stdscr.getch()
        if key_pressed == ord('q'):
            exit_menu = True

def main_menu(stdscr):
    # turn off cursor blinking
    curses.curs_set(0)

    # color scheme for selected row
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # specify the current selected row
    current_row = 0

    # print the Info.menu
    print_menu(stdscr, current_row)

    in_menu = True

    while in_menu:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(Info.menu)-1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                main(stdscr)
            elif current_row == 1:
                show_rules(stdscr)
            elif current_row == 2:
                break  

        print_menu(stdscr, current_row)

if __name__ == "__main__":
    curses.wrapper(main_menu)
