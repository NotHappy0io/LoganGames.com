def grid(x,y):
    game = []
    for i in range(0,x):
        for j in range(0,y):
            game.append([i,j])
    return game

my_grid = grid(5, 10)
print(my_grid) # You need this to see the result