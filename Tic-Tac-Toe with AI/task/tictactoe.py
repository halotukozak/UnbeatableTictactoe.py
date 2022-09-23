import random
from tic_tac_toe_exceptions import InvalidCoordinatesException, OccupiedCellException


class Game:
    win_cases = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]

    def __init__(self):
        self.X_moves = set()
        self.O_moves = set()

        self.curr_turn = "X"
        self.run()

    @classmethod
    def calculate_cell(cls, x, y):
        return {1: {1: 0, 2: 1, 3: 2}, 2: {1: 3, 2: 4, 3: 5}, 3: {1: 6, 2: 7, 3: 8}}[x][y]

    @classmethod
    def print_ai_move(cls, level):
        print(f'Making move level "{level}"')

    @classmethod
    def is_won_by(cls, player_moves):
        return any([all([win_move in player_moves for win_move in win_case]) for win_case in Game.win_cases])

    def game_is_finished(self):
        if Game.is_won_by(self.get_current_moves()):
            print(f"{self.curr_turn} wins")
            return True

        available_indices = Game.get_spots(self.X_moves, self.O_moves)
        if not available_indices:
            print("Draw")
            return True
        return False

    def get_current_moves(self):
        return self.X_moves if self.curr_turn == "X" else self.O_moves

    def get_opponent_moves(self):
        return self.X_moves if self.curr_turn == "O" else self.O_moves

    @classmethod
    def get_spots(cls, moves1, moves2):
        return {x for x in range(9)} - moves1 - moves2

    def save_move(self, cell_number):
        curr_moves = self.get_current_moves()
        curr_moves.add(cell_number)

    def generate_board(self):
        board = [i for i in range(9)]
        for x_move in self.X_moves:
            board[x_move] = "X"
        for o_move in self.O_moves:
            board[o_move] = "O"

        return board

    def print_board(self):
        board = [" " if type(cell) == int else cell for cell in self.generate_board()]

        print(
            "---------\n"
            + f"| {board[0]} {board[1]} {board[2]} |\n"
            + f"| {board[3]} {board[4]} {board[5]} |\n"
            + f"| {board[6]} {board[7]} {board[8]} |\n"
            + f"--------- "
        )

    def change_turn(self):
        self.curr_turn = "O" if self.curr_turn == "X" else "X"

    def get_user_move(self):
        x, y = [int(a) for a in input("Enter the coordinates:").split()]
        if x not in (1, 2, 3) or y not in (1, 2, 3):
            raise InvalidCoordinatesException
        cell_number = Game.calculate_cell(x, y)
        if cell_number in self.O_moves.union(self.X_moves):
            raise OccupiedCellException
        return cell_number

    def get_random_move(self):
        return random.choice(list(self.get_spots(self.get_current_moves(), self.get_opponent_moves())))

    def get_easy_move(self):
        Game.print_ai_move("easy")
        return self.get_random_move()

    def get_medium_move(self):
        Game.print_ai_move("medium")
        for moves in (self.get_current_moves(), self.get_opponent_moves()):
            if len(moves) > 1:
                for win_case in Game.win_cases:
                    missing_cells = win_case - moves
                    missing_cell = missing_cells.pop()
                    if not missing_cells and missing_cell not in self.X_moves.union(self.O_moves):
                        return missing_cell
        return self.get_random_move()

    def get_hard_move(self):
        def minimax(player_moves, opponent_moves, turn):
            available_indices = Game.get_spots(player_moves, opponent_moves)
            if Game.is_won_by(opponent_moves):
                return {"score": -10}
            elif Game.is_won_by(player_moves):
                return {"score": 10}
            elif not available_indices:
                return {"score": 0}

            moves = {}

            curr_moves = self.X_moves if turn == "X" else self.O_moves

            for available_index in available_indices:
                curr_moves.add(available_index)
                if turn == self.curr_turn:
                    result = minimax(player_moves, opponent_moves, "X" if self.curr_turn == "O" else "O"
                                     )
                else:
                    result = minimax(player_moves, opponent_moves, self.curr_turn)

                curr_moves.remove(available_index)

                moves[available_index] = result["score"]

            best_move = int
            best_score = max(moves.values()) if turn == self.curr_turn else min(moves.values())

            for move, score in moves.items():
                if score == best_score:
                    best_move = move
                    break

            return {"best_move": best_move, "score": best_score}

        Game.print_ai_move("hard")
        return minimax(self.get_current_moves(),
                       self.get_opponent_moves(),
                       self.curr_turn)["best_move"]

    def run(self):
        self.print_board()
        while True:
            try:
                curr_player = player_x if self.curr_turn == "X" else player_o

                if curr_player == "user":
                    cell_number = self.get_user_move()
                elif curr_player == "medium":
                    cell_number = self.get_medium_move()
                elif curr_player == "hard":
                    cell_number = self.get_hard_move()
                else:
                    cell_number = self.get_easy_move()

                self.save_move(cell_number)
                self.print_board()
                if self.game_is_finished():
                    break
                self.change_turn()

            except ValueError:
                print("You should enter the numbers!")

            except Exception as e:
                print(e)


while True:
    try:
        inp = input("Input command:")

        if inp == "exit":
            break
        else:
            player_x, player_o = inp.split()[1:]
            Game()
    except ValueError:
        print("Bad parameters!")
