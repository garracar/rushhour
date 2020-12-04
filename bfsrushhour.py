from rhboard import RHBoard
from plotting import plot_solution
import numpy as np
import datetime

def BFS_RushHour(board):
    original_node = (0, (0, 0), board)

    queue = []
    path_vector = []

    path_vector.append(original_node)

    queue.append(path_vector)
    all_status = set()
    while queue:
        current_path = queue.pop(0)
        new_tablero = current_path[-1][2]

        if new_tablero.is_final_position():
            return current_path

        for next_element in new_tablero.get_following_boards():
            tablero_tup = next_element[2].board_tuple
            if tablero_tup not in {xx[2].board_tuple for xx in current_path} and tablero_tup not in all_status:
                all_status.add(tablero_tup)
                new_path = [xx for xx in current_path]
                new_path.append(next_element)
                queue.append(new_path)

    return None


if __name__ == "__main__":
    file_path = r'boards_example\RushHour48.txt'

    rhb = RHBoard.get_board_from_file(file_path)

    print("[{}]: Start".format(datetime.datetime.now()))
    res = BFS_RushHour(rhb)
    print("[{}]: End".format(datetime.datetime.now()))

    plot_solution(res, 200)
