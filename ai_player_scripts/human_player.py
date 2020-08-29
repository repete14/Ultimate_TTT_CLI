import UTTT


class Player:

   def __init__(self,symbol):
       self.name = "human"
       self.symbol = symbol

    def get_move(self, board, legal_moves):
        try:
            if len(target_boards) > 1:
                print("\n7|8|9\n-+-+-\n4|5|6\n-+-+-\n1|2|3")
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
        if move.get_coord_string() not in legal_moves:
            logging.error("NOPE. not legal, try again, cheater pants!!")
            move = None