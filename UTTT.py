#!/usr/bin/env python3
from os import system
import argparse
import logging


def main():
    game_board = Board()
    current_player = "X"
    last_move = None
    legal_moves = []

    while not game_board.winner:
        target_boards = get_target_boards(game_board, last_move)
        legal_moves = get_legal_moves(target_boards)
        logging.debug(f"legal moves: {legal_moves}")
        display_game(game_board, legal_moves, last_move)
        move = get_move(current_player, target_boards, legal_moves)
        make_move(game_board, move)
        game_board.update_winners(move)
        last_move = move
        current_player = switch_players(current_player)

    display_game(game_board, legal_moves, last_move)
    print(f"\n\nPlayer {game_board.winner} has won!! way to kick ass!!!!!")


def get_target_boards(game_board, last_move):
    if not last_move or game_board.sub_boards[last_move.x][last_move.y].winner:
        return game_board.get_available_boards()
    else:
        return [game_board.sub_boards[last_move.x][last_move.y]]


def get_legal_moves(available_sub_boards):
    return [space.get_coordinates() for sub_board in available_sub_boards for space in sub_board.get_available_spaces()]


def get_move(player, target_boards, legal_moves):
    move = None
    color = Color
    if player == "X":
        formatter = f"{color.RED}"
    else:
        formatter = f"{color.BLUE}"

    while not move:
        try:
            if len(target_boards) > 1:
                result = input(f"\nplayer {formatter}{player}{color.END}, select sub-board (1-9): ")
                sub_board = get_coordinate(int(result))
            else:
                sub_board = (target_boards[0].x, target_boards[0].y)

            result = input(f"\nplayer {formatter}{player}{color.END}, select move (1-9): ")

            if result == "0":
                logging.error("Counting to 9 isn't your strong suit, is it. Try again")
                continue
            if result == "q":
                logging.warning("Quitting game now....quitter")
                exit()

            space = get_coordinate(int(result))
        except ValueError:
            logging.error("not a valid input. Ya dun fucked up. try again")
            continue
        except IndexError:
            logging.error("Counting to 9 isn't your strong suit, is it. Try again")
            continue

        move = Move(sub_board[0], sub_board[1], space[0], space[1], player)
        if move.get_coordinates() not in legal_moves:
            logging.error("NOPE. not legal, try again, cheater pants!!")
            move = None

    return move


def make_move(game_board, move):
    game_board.sub_boards[move.gx][move.gy].spaces[move.x][move.y].winner = move.player


def check_grid_for_winner(grid, move):
    if move.player:
        for x in range(3):
            # Vertical win check
            if len([row[x].winner for row in grid if row[x].winner == move.player]) == 3:
                return True

            # horizontal win check
            if len([space.winner for space in grid[x] if space.winner == move.player]) == 3:
                return True

        # Diagonal win check
        if len([grid[x][x].winner for x in range(3) if grid[x][x].winner == move.player]) == 3:
            return True
        if len([grid[x][2 - x].winner for x in range(3) if grid[x][2 - x].winner == move.player]) == 3:
            return True

    return False


def switch_players(player):
    if player == "X":
        return "O"
    else:
        return "X"


def display_game(board, legal_moves, last_move):
    divider_game_corner = " "
    divider_game_row = " "
    divider_game_col = "   "
    divider_sub_corner = "-+-"
    divider_sub_row = "-"
    divider_sub_col = " | "
    color = Color
    grid_display_type = ["v", "s", "v", "s", "v", "g", "v", "s", "v", "s", "v", "g", "v", "s", "v", "s", "v"]
    grid_display_reference = {"gg": divider_game_corner,
                              "gv": divider_game_row,
                              "gs": divider_game_row,
                              "vg": divider_game_col,
                              "vv": None,
                              "vs": divider_sub_col,
                              "sg": divider_game_col,
                              "sv": divider_sub_row,
                              "ss": divider_sub_corner}

    display_grid = []
    if not args.debug:
        _ = system("clear")

    for row in range(17):
        display_grid.append("")
        for col in range(17):
            sub_board = board.sub_boards[int(col / 6)][int(row / 6)]
            space = sub_board.spaces[int((col / 2) % 3)][int((row / 2) % 3)]
            cell_type_code = f"{grid_display_type[row]}{grid_display_type[col]}"

            if grid_display_reference[cell_type_code]:
                cell_value = f"{grid_display_reference[cell_type_code]}"
                if sub_board.winner == "X":
                    cell_value = f"{color.RED}{cell_value}{color.END}"
                elif sub_board.winner == "O":
                    cell_value = f"{color.BLUE}{cell_value}{color.END}"

            else:
                formatting = ""
                cell_value = space.get_display()

                if space.get_coordinates() in legal_moves:
                    cell_value = f"{get_key((space.x, space.y))}"
                    formatting += f"{color.GREEN}"
                elif space.get_coordinates() == last_move.get_coordinates():
                    formatting += f"{color.UNDERLINE}"

                if space.winner == "X":
                    formatting += f"{color.RED}"
                elif space.winner == "O":
                    formatting += f"{color.BLUE}"

                cell_value = f"{formatting}{cell_value}{color.END}"
            display_grid[row] += cell_value

    for line in display_grid:
        print(line)


def get_coordinate(key):
    lookup = [(0, 2), (1, 2), (2, 2),
              (0, 1), (1, 1), (2, 1),
              (0, 0), (1, 0), (2, 0)]
    return lookup[key - 1]


def get_key(coordinate):
    lookup = [[7, 4, 1],
              [8, 5, 2],
              [9, 6, 3]]
    return lookup[coordinate[0]][coordinate[1]]


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Space:
    def __init__(self, x, y, parent):
        self.winner = None
        self.x = x
        self.y = y
        self.key = get_key((self.x, self.y))
        self.parent = parent
        self.last_move = False
        self.allowed = True

    def get_display(self):
        return self.winner or " "

    def get_coordinates(self):
        return f"{self.parent.x}{self.parent.y}{self.x}{self.y}"


class SubBoard:
    def __init__(self, x, y, parent):
        self.winner = None
        self.x = x
        self.y = y
        self.key = get_key((self.x, self.y))
        self.parent = parent
        self.spaces = []

        for i in range(3):
            self.spaces.append([])
            for j in range(3):
                self.spaces[i].append(Space(i, j, self))

    def get_available_spaces(self):
        return [space for sub in self.spaces for space in sub if not space.winner]

    def update_winners(self, move):
        self.winner = move.player
        if move.player == "X":
            symbol = [["\\", " ", "/"],
                      [" ", "X", " "],
                      ["/", " ", "\\"]]
        else:
            symbol = [["/", "|", "\\"],
                      ["-", " ", "_"],
                      ["\\", "|", "/"]]
        for x in range(3):
            for y in range(3):
                self.spaces[x][y].winner = symbol[x][y]


class Board:
    def __init__(self):
        self.winner = None
        self.sub_boards = []

        for i in range(3):
            self.sub_boards.append([])
            for j in range(3):
                self.sub_boards[i].append(SubBoard(i, j, self))

    def get_available_boards(self):
        return [board for sub in self.sub_boards for board in sub if not board.winner]

    def update_winners(self, move):
        impacted_board = self.sub_boards[move.gx][move.gy]
        logging.debug(f"checking board {impacted_board.key} for winning move")
        if check_grid_for_winner(impacted_board.spaces, move):
            logging.debug(f"winner found in board {impacted_board.key} with move {move.key}")
            impacted_board.update_winners(move)
            if check_grid_for_winner(self.sub_boards, move):
                logging.debug(f"winner found for game with move {move.key}")
                self.winner = move.player


class Move:
    def __init__(self, gx, gy, x, y, player):
        self.gx = gx
        self.gy = gy
        self.gkey = get_key((self.gx, self.gy))
        self.x = x
        self.y = y
        self.key = get_key((self.x, self.y))
        self.player = player

    def get_coordinates(self):
        return f"{self.gx}{self.gy}{self.x}{self.y}"


def setup():
    description_text = "hotseat, CLI implementation of Ultimate Tic Tac Toe"
    parser = argparse.ArgumentParser(description_text)
    parser.add_argument("-V", "--version", help=" show program version", action="store_true")
    parser.add_argument("-d", "--debug", help=" display debug info", action="store_true")
    parsed_args = parser.parse_args()

    if parsed_args.debug:
        logging.basicConfig(level=logging.DEBUG)

    return parsed_args


if __name__ == "__main__":
    args = setup()
    main()
