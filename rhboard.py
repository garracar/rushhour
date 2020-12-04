import numpy as np
import pandas as pd

class RHBoard():
    def __init__(self, board):
        # Establish the board
        self.board = board

        # Get the end position
        self.board_shape = board.shape
        self.end_pos = (np.where(self.board == -1)[0][0], self.board_shape[1]-1)
        
        # Get the status
        self.board_status = self.__get_board_status()

    def __repr__(self):
        return str(self.board_tuple)

    @property
    def board_tuple(self):
        return tuple(map(tuple, self.board))

    def is_final_position(self):
        """
        Decides whether a position is an end position.
        In order to be final position, the red car should be at the right of the board
        :return: True or false
        """
        if self.board[self.end_pos] == -1:
            return True
        else:
            return False

    def __get_board_status(self):
        """
        Determines the status of the board
        :return: Dictionary for each car giving starting point, vertical / horizontal, size
                 and the list of possible positions
        """
        d_elems = {}
        V_H = None
        for i, x in enumerate(self.board):
            for j, y in enumerate(x):
                if y != 0 and y not in d_elems:
                    valid_movements = []
                    # Try to move vertical
                    try:
                        if self.board[i + 1, j] == y:
                            V_H = 'V'
                        else:
                            V_H = 'H'
                    except:
                        V_H = 'H'

                    # Movements (vertical up / down)
                    len_car = np.count_nonzero(self.board == y)
                    if V_H == 'V':
                        try:
                            if self.board[i + len_car, j] == 0:
                                valid_movements.append((i + 1, j))
                        except:
                            pass

                        try:
                            if i > 0 and self.board[i - 1, j] == 0:
                                valid_movements.append((i - 1, j))
                        except:
                            pass
                    # Horizontal (Left / Right)
                    else:
                        try:
                            if self.board[i, j + len_car] == 0:
                                valid_movements.append((i, j + 1))
                        except:
                            pass

                        try:
                            if j > 0 and self.board[i, j - 1] == 0:
                                valid_movements.append((i, j - 1))
                        except:
                            pass

                    d_elems[y] = ((i, j), V_H, len_car, valid_movements)
        return d_elems

    def get_following_boards(self):
        res = []

        for car, (init_pos, V_H, len_car, valid_movements) in self.board_status.items():
            for mov in valid_movements:
                new_dict = self.board_status.copy()
                new_dict[car] = (mov, V_H, len_car, valid_movements)

                new_tablero = RHBoard.get_board_from_dict(new_dict, self.board_shape)

                res.append((car, mov, new_tablero))

        return res

    @classmethod
    def get_board_from_file(cls, file):
        """
        Get a board class using a file
        :param file: File reference
        :return: Board
        """
        # 1) Read file
        df = pd.read_csv(file, header=None)
        board = df.values

        return cls(board)

    @classmethod
    def get_board_from_dict(cls, dct_board, shape):
        """
        Generates a board given a dictionary.
        :param dct_board: key: car_number (-1 is the goal) //
        values: origin, 'V': Vertical / 'H': Horizontal, size of the car)
        :param shape: tuple with the shape of the board
        :return: A RHBoard object
        """
        new_board = np.zeros(shape, dtype=int)

        for car, prop in dct_board.items():
            ini_pos = prop[0]
            V_H = prop[1]
            car_len = prop[2]

            if V_H == 'V':
                new_board[ini_pos[0]:(ini_pos[0]+car_len), ini_pos[1]] = car
            else:
                new_board[ini_pos[0], ini_pos[1]:(ini_pos[1] + car_len)] = car

        return cls(new_board)

if __name__ == "__main__":
    import os

    file_path = r'boards_example\RushHour48.txt'

    rhb = RHBoard.get_board_from_file(file_path)
    kk = rhb.get_following_boards()


    pass