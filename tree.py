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
first_time = True


class A_star:

    def __init__(self, grid_size, position, goal_position, mapp):
        self.grid_size = grid_size
        self.position = self.agent_pos = position
        self.destination = goal_position
        self.map = mapp

    def expand(self, pos):
        global first_time
        flag = True
        #minimum = 0
        #min_index = 0
        frontier_index = 0
        cost_parent = -1

        actions = {"UP": (pos[0]-1, pos[1]), "DOWN": (pos[0]+1, pos[1]),
                   "LEFT": (pos[0], pos[1]-1), "RIGHT": (pos[0], pos[1]+1)}

        if first_time:
            price = self.f_n(None, 0, pos, self.destination)
            frontier.append([pos, None, price, None])
            first_time = False
        else:
            if pos[0] == 0:
                actions["UP"] = (-1, -1)
            elif pos[0] == self.grid_size - 1:
                actions["DOWN"] = (-1, -1)
            if pos[1] == 0:
                actions["LEFT"] = (-1, -1)
            elif pos[1] == self.grid_size - 1:
                actions["RIGHT"] = (-1, -1)

            for act_key in actions:
                explored_flag = False
                if actions[act_key] != (-1, -1):
                    if self.map[actions[act_key][0]][actions[act_key][1]] != '*':
                        for ex_node in range(len(explored)):
                            if explored[ex_node][0] == pos:
                                cost_parent = explored[ex_node][2]
                            if actions[act_key] == explored[ex_node][0]:
                                explored_flag = True
                        if not explored_flag:
                            price = self.f_n(pos, cost_parent, actions[act_key], self.destination)
                            for node in range(len(frontier)):
                                """if min_index == 0:
                                    minimum = frontier[node][2]
                                    min_index = 1"""
                                if frontier[node][0] == actions[act_key] and frontier[node][2] > price:
                                    frontier[node][2] = price
                                    frontier[node][1] = pos
                                    frontier[node][3] = act_key
                                    flag = False
                                    break
                            if flag:
                                frontier.append([actions[act_key], pos, price, act_key])

        minimum = frontier[0][2]
        for node in range(len(frontier)):
            if frontier[node][2] < minimum:
                minimum = frontier[node][2]
        while True:
            if frontier[frontier_index][2] == minimum:
                if frontier[frontier_index][0] == self.destination:
                    global dest_pos, dest_cost
                    dest_pos, dest_cost = frontier[frontier_index][0], frontier[frontier_index][2]
                    break
                else:
                    explored.append(frontier[frontier_index])
                    frontier.pop(frontier_index)
                    self.expand(explored[len(explored)-1][0])
                    break
            frontier_index += 1

    def f_n(self, parent, parent_cost, position, goal_position):
        """global costt
        costt = 0
        for node in explored:
            if node[0] == parent:
                costt = node[2] + 1
        """
        if not parent:
            g_n = 0
        else:
            parent_hn = (abs(goal_position[0] - parent[0])) + (abs(goal_position[1] - parent[1]))
            g_n = (parent_cost - parent_hn) + 1
        h_n = (abs(goal_position[0] - position[0])) + (abs(goal_position[1] - position[1]))
        return g_n + h_n

    def solution(self, pos):
        global dest_pos, dest_cost
        self.expand(pos)
        for ex in range(len(explored)):
            if explored[ex][0] == dest_pos:
                path.index(0, explored[ex][2])
                dest_pos = explored[ex][1]
        return path, dest_cost
