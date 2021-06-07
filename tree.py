"""class Node:

    def __init__(self, position, parent, cost, action):
        self.position = position
        self.parent = parent
        self.cost = cost
        self.action = action
"""


frontier = list()
explored = list()
path = list()

dest_pos = tuple()
dest_cost = -1


class A_star:
    #destination = None

    def __init__(self, grid_size, position, goal_position, mapp):
        self.grid_size = grid_size
        self.position = position
        self.destination = goal_position
        self.map = mapp

    def expand(self, pos):

        actions = {"UP": (pos[0]-1, pos[1]), "DOWN": (pos[0]+1, pos[1]),
                   "LEFT": (pos[0], pos[1]-1), "RIGHT": (pos[0], pos[1]+1)}

        if not frontier:
            price = self.f_n(None, pos, self.destination)
            frontier.append([pos, None, price, None])

        if pos[0] == 0:
            actions["UP"] = (-1, -1)
        elif pos[0] == self.grid_size - 1:
            actions["DOWN"] = (-1, -1)
        if pos[1] == 0:
            actions["LEFT"] = (-1, -1)
        elif pos[1] == self.grid_size - 1:
            actions["RIGHT"] = (-1, -1)

        explored_flag = False
        flag = True
        minimum = 0
        min_index = 0
        #for act_key, act_value in actions.items():
        for act_key in actions:
            #global flag, minimum, min_index, explored_flag
            if actions[act_key] != (-1, -1): #[0] != -1 and actions[act_key][1] != -1:
                if self.map[actions[act_key][0]][actions[act_key][1]] != '*':
                    for ex_node in range(len(explored)):
                        if actions[act_key] == explored[ex_node][0]:
                            explored_flag = True
                    if not explored_flag:
                        price = self.f_n(pos, actions[act_key], self.destination)
                        for node in range(len(frontier)):
                            if min_index == 0:
                                minimum = frontier[node][2]
                                min_index = 1
                            if frontier[node][0] == actions[act_key] and frontier[node][2] > price:
                                frontier[node][2] = price
                                frontier[node][1] = pos
                                frontier[node][3] = act_key
                                flag = False
                                break
                        if flag:
                            frontier.append([actions[act_key], pos, price, act_key])

        for node in range(len(frontier)):
            if frontier[node][2] < minimum:
                minimum = frontier[node][2]
        for node in range(len(frontier)):
            if frontier[node][2] == minimum:
                if frontier[node][0] == self.destination:
                    global dest_pos, dest_cost
                    dest_pos, dest_cost = frontier[node][0], frontier[node][2]
                else:
                    explored.append([frontier[node]])
                    frontier.pop(node)
                    self.expand(frontier[node][0])
                    break

    def f_n(self, parent, position, goal_position):
        global costt
        costt = 0
        for node in explored:
            if node[0] == parent:
                costt = node[2]
        g_n = 1 + costt
        h_n = (abs(goal_position[0] - position[0])) + (abs(goal_position[1] - position[1]))
        return g_n + h_n

    def solution(self, pos):
        global dest_pos, dest_cost
        self.expand(pos)
        for ex in explored:
            if ex.position == dest_pos:
                path.index(0, ex.action)
                dest_pos = ex.parent
        return path, dest_cost
