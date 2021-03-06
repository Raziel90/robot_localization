# ----------
# User Instructions:
#
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's
# optimal path to the position specified in goal;
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a
# right turn.

forward = [[-1, 0],  # go up
           [0, -1],  # go left
           [1, 0],  # go down
           [0, 1]]  # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0]  # given in the form [row,col,direction]
# direction = 0: up
#             1: left
#             2: down
#             3: right

goal = [2, 0]  # given in the form [row,col]

cost = [2, 1, 20]  # cost has 3 values, corresponding to making


grid = [[0, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [4, 5, 0]
goal = [4, 3]
cost = [1, 1, 1]
# a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def node_expand(node,closed,grid,value,cost):
    isvalid = lambda x,y: 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0
    c, a, x, y, t = node
    expansion = []
    for move in forward:
        x2 = x + move[0]
        y2 = y + move[1]
        if isvalid(x2,y2):
            for orient, dir in enumerate(forward):
                for act in action:
                    c2 = c + cost[act + 1]
                    if forward[(orient+act)%4][0] + x2 == x and forward[(orient+act)%4][1] + y2 == y and (orient + act) % 4 == t:
                        if isvalid(x2 + forward[(orient+2)%4][0],y2 + forward[(orient+2)%4][1]) or init==[x2,y2,orient]:
                            if value[x2][y2][orient] > c2 and [x, y, t] not in closed:
                                # if x2 == 1 and y2 == 3:
                                #     print(c2,'x,y,t=', x, y, t, ' action: ', action_name[act + 1], orient)
                                expansion.append([c2, act, x2, y2, orient])
    return expansion

def optimum_policy2D(grid, init, goal, cost):
    isvalid = lambda x, y: 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0
    value = [[[999 for k in range(len(forward))] for i in range(len(grid[0]))] for j in range(len(grid))]
    policy = [[[" " for k in range(len(forward))] for i in range(len(grid[0]))] for j in range(len(grid))]
    policy2D = [[" " for i in range(len(grid[0]))] for j in range(len(grid))]
    value[goal[0]][goal[1]] = [0 for k in range(len(forward))]  # goal value is zero

    #find orient in goal
    goal_dir = [(dir + 2) % 4 for dir, mov in enumerate(forward) if isvalid(mov[0] + goal[0], mov[1] + goal[1])][0]
    closed = []
    expanded = []
    expanded.append([0, -2, goal[0],goal[1], goal_dir])
    while len(expanded) > 0:
        node = expanded.pop(0)
        c, a, x, y, t = node
        expansion = node_expand(node, closed, grid, value, cost)
        expanded += expansion

        expanded.sort()
        m = min(value[x][y])
        value[x][y][t] = c

        closed.append((c,[x,y,t]))
        if a == -2:
            policy[x][y][t] = '*'
        elif c < m:
            policy[x][y][t] = action_name[a + 1]

    x,y,t = init
    policy2D[x][y] = policy[x][y][t]
    while (x,y) != goal:
        print(x,y,t)
        if policy[x][y][t] == '#':
            o = t
            print('#')
        elif policy[x][y][t] == 'L':
            o = (t + 1) % 4
            print('L')
        elif policy[x][y][t] == 'R':
            o = (t - 1) % 4
            print('R')
        #print(x, y, t, (o - t)%4)
        x = x + forward[o][0]
        y = y + forward[o][0]
        t = o
        policy2D[x][y] = policy[x][y][t]
    return policy2D#, closed

pol= optimum_policy2D(grid, init, goal, cost)
print([str(i) if i >=0 else " " for i in range(-1,len(pol[0]))])
[print([j]+p) for j,p in enumerate(pol)]
#[print(p) for p in path]
