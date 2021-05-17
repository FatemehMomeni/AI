frontier = []
explored = []


class Node:

    def __init__(self, position, parent):
        self.position = position ## root
        #self.children = []
        self.parent = parent


class a:
    destination = None

    def __init__(self, grid_size, position, goal_position):
        self.grid_size = grid_size
        self.position = position
        self.destination = goal_position
        self.expand(self.position)

    def expand(self, position):
        actions = [(position[0]-1, position[1]), (position[0]+1, position[1]),
                   (position[0], position[1]-1), (position[0], position[1]+1)]
        if not frontier:
            cost = self.f_n(position, self.destination)
            frontier.append([position, cost])
            root = Node(position, None)
        else:
            if position[0] == 0:
                actions.pop(0)
            elif position[0] == self.grid_size - 1:
                actions.pop(1)
            if position[1] == 0:
                actions.pop(2)
            elif position[1] == self.grid_size - 1:
                actions.pop(3)
        for act in actions:
            if act != '*':
                if act not in explored:
                    cost = self.f_n(act, self.destination)
                    node = Node(act, position)
                    if act not in frontier:
                        frontier.append([act, cost])
                    else:
                        i = frontier.index(act)
                        frontier[i][1] = cost
        min = frontier[0][1]
        for i in range(len(frontier)):
            if frontier[i][1] < min:
                self.expand(frontier[i][0])
                frontier.pop(i)

    def f_n(self, position, goal_position):
        # add cost of parents in g_n       "REMEMBER"
        i = frontier.index(position)
        g_n = 1 + frontier[i][1]
        h_n = (abs(goal_position[0] - position[0])) + (abs(goal_position[1] - position[1]))
        return g_n + h_n
