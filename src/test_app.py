import pytest
import numpy
from unittest.mock import patch
from queens import main, matriz_size, board_generator, print_board, posibilities, exist_solutions, insert_boards, create_table, solutions_count
import logging
from sqlalchemy import create_engine, Column, Integer, String, MetaData, func, Table, ARRAY, JSON, distinct


#Database configuration
DB_URL = "postgresql+psycopg2://admin:admin@host.docker.internal:5432/boards"
engine = create_engine(DB_URL)
metadata = MetaData()
table = create_table(engine, metadata)


#Tamaño de matriz
"""def test_matriz_size():

    for n in range(1,11):
        with patch('builtins.input', return_value=n):
            assert matriz_size() == n"""

#
def test_initialization(monkeypatch):
    for i in range(1,9):
        monkeypatch.setattr('builtins.input', lambda _: i)
        main()
    """
    monkeypatch.setattr('builtins.input', lambda _: 5)
        #assert matriz_size() == size
    size = matriz_size()

    board = board_generator(size,size)
    print_board(board)

    start = 0
    list_p = posibilities(board, start)

    if exist_solutions(size, engine, table):
        insert_boards(size, list_p, engine, table)
    else:
        print("This solution is stored in database!")


"""

@pytest.mark.parametrize(
    "size_board, res",
    [   
        (1, 1),
        (2, 0),
        (3, 0),
        (4, 2),
        (5, 10),
        (6, 4),
        (7, 40),
        (8, 92)
    ]
)
def test_queen_n(size_board, res):
    assert solutions_count(size_board) == res
    




    