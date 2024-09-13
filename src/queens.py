import json
from sqlalchemy import create_engine, Column, exists, Integer, String, MetaData, func, Table, ARRAY, JSON, distinct
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import insert, select
import numpy as np
import builtins


#Database configuration
DB_URL = "postgresql+psycopg2://admin:admin@host.docker.internal:5432/boards"
engine = create_engine(DB_URL)
metadata = MetaData()

#Create table in DB boards
def create_table(engine, metadata):    

    boards = Table('boards', metadata,
                Column('id', Integer, primary_key=True),
                Column('size', String), #This field is for count the boards with same size (solutions numbers)
                Column('board', JSON) #Matriz se guarda como tipo JSON (This field is a JSON width this we can save the matrix)
    )
    metadata.create_all(engine)
    return boards


#Set matrix with size giving for the user
def matriz_size():
    print("Eight Queen puzzle")
    size = int(input("What size do you want your board? "))
    print(f"Your board is: {size}")
    return size


#empty board creation
def board_generator(rows, columns):
    board = []

    for i in range(rows):
        row = []
        for j in range(columns):
            value = '·'
            row.append(value)
        board.append(row)
    return board

def print_board(board):
    for row in board:
        print(" | ".join(map(str, row))) #Convert element to text
        print("-" * (len(row) * 4 - 1 )) #lenght of separator


def put_queen(board, row, start):

    for i in range(start):
        if board[row][i] == '*': #this meaning the algorith found a queen
            return False #It says the queen cannot put in the place

    #the queen starts in (0,0) for that reason we just check left side in search of queen
    #We are assuming there are no queens on right

    a = row
    b = start
    while a >= 0 and b >= 0:
        if board[a][b] == '*':
            return False
        a = a - 1 #Si no hay una reina en la posición, retrocedemos una fila
        b = b - 1 #Si no hay una reina en la posición, retrocedemos una columna

    c = row
    d = start
    while c < len(board) and d >= 0:
        if board[c][d] == '*':
            return False
        c = c + 1 #Si no hay una reina en la posición, avanzamos una fila
        d = d - 1 #Si no hay una reina en la posición, retrocedemos una columna
    return True
            
def iteration_board(board, start, p_list):

    if start >= len(board):
        p_list.append([row.copy() for row in board]) #Copy of the board in my list
        return

    for i in range(len(board)):
        if put_queen(board, i, start):
            board[i][start] = '*'
            iteration_board(board, start + 1, p_list)
            board[i][start] = '·'

        

def posibilities(board, start):
    #list of posibilities of board
    p = []

    iteration_board(board, start, p)
    
    return p    

def create_table(engine, metadata):    

    boards = Table('boards', metadata,
                Column('id', Integer, primary_key=True),
                Column('size', String), #Con un count sabremos el número de soluciones para N size
                Column('board', JSON) #Matriz se guarda como tipo JSON
    )

    metadata.create_all(engine)
    return boards

def exist_solutions(n, engine, table_name):
    n=str(n)
    Session = sessionmaker(bind=engine)
    session = Session()

    in_table = session.query(exists().where(table_name.c.size == n)).scalar()

    """with engine.connect() as connection:
        query = select([table_name.c.size]).where(table_name.c.size == size)
        in_table = connection.execute(select([exist(query)])).scalar()"""
    return in_table


#Insert the boards like json data
def insert_boards(size, list_p, engine, table):
    #loop to the list
    for x in list_p:
        with engine.connect() as connection:
            trans = connection.begin()            
            try:                
                insert_board = insert(table).values(
                    size = size,
                    board = x
                )
                connection.execute(insert_board)
                trans.commit()
                # Verificar la inserción
                """select_stmt = table.select()
                result = connection.execute(select_stmt)
                for row in result:
                    print(row)"""
            except Exception as e:
                trans.rollback()
                print(f"Errorrr: {e}")

def solutions_count(size_board):
    size_board = str(size_board)
    #Database configuration
    DB_URL = "postgresql+psycopg2://admin:admin@host.docker.internal:5432/boards"
    engine = create_engine(DB_URL)
    metadata = MetaData()
    boards = create_table(engine, metadata)

    with engine.connect() as connection:
        t = connection.begin()
        query = select(func.count()).select_from(boards).where(boards.c.size == size_board)
        result = connection.execute(query)
        d = result.mappings().all()
        return d[0]['count_1']


def get_boards(size):    
    size = str(size)
    
    boards = Table('boards', metadata, autoload_with=engine)

    with engine.connect() as connection:
        query = select(boards.c.board).where(boards.c.size == size)
        result = connection.execute(query)
        rows_as_lists = [list(row) for row in result]
        for row_list in rows_as_lists:
            for row in row_list:
                print("\n")
                print_board(row)


def main():   

    print("¡Bienvenido!")
    
    #Ask to the user board size
    size = matriz_size()

    #board generator size of parameter
    board = board_generator(size, size)
    print("board")
    print(board)
    #print board
    print_board(board)

    #initial position of queen
    start = 0
    list_p = posibilities(board, start)
    #print("soluciones posibles:")
    #print(list_p)

    #Database configuration
    DB_URL = "postgresql+psycopg2://admin:admin@host.docker.internal:5432/boards"
    engine = create_engine(DB_URL)
    metadata = MetaData()
    table_name = create_table(engine, metadata)

    if exist_solutions(size, engine, table_name):
        print("This solution is stored in database!")        
    else:
        insert_boards(size, list_p, engine, table_name)

    solutions_count(size)

    get_boards(size)


    

    

if __name__ == "__main__":
    main()