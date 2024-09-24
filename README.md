This is the N queens algorithm.

The main function ask to the user for a size board.

Before execute the algorithm we will validate if the solutions of that size is in the postgres database,
If true, pull the boards posibilities to print, If False, the algorithm execute all the posibilities according the size
and store them on postgres database.

For the installation, you need clone the repository and execute docker-compose for up two images: postgres and principal app.

Automatically the app execute test about solutions for the puzzle.
