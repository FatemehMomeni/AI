class Node:

    def __init__(self, position, parent, cost, action):
        self.position = position
        self.parent = parent
        self.cost = cost
        self.action = action


frontier = list[Node]
explored = list[Node]
path = list()


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
        else:
            if pos[0] == 0:
                actions["UP"] = (0, 0)
            elif pos[0] == self.grid_size - 1:
                actions["DOWN"] = (0, 0)
            if pos[1] == 0:
                actions["LEFT"] = (0, 0)
            elif pos[1] == self.grid_size - 1:
                actions["RIGHT"] = (0, 0)

        explored_flag = False
        flag = True
        minimum = 0
        min_index = 0
        for act_key, act_value in actions.items():
            #global flag, minimum, min_index, explored_flag
            if act_value != (0, 0) and self.map[self.grid_size * act_value[0] + act_value[1]] != '*':
                for ex_node in explored:
                    if act_value == ex_node.position:
                        explored_flag = True
                if not explored_flag:
                    price = self.f_n(pos, act_value, self.destination)
                    for node in frontier:
                        if min_index == 0:
                            minimum = node.cost
                            min_index = 1
                        if node.position == act_value and node.cost > price:
                            node.cost = price
                            node.parent = pos
                            node.action = act_key
                            flag = False
                            break
                    if flag:
                        frontier.append([act_value, pos, price, act_key])

        for node in frontier:
            if node.cost < minimum:
                minimum = node.cost
        for node in frontier:
            if node.cost == minimum:
                if node.position == self.destination:
                    return node.position, node.cost
                else:
                    self.expand(node.position)
                    frontier.pop(node)
                    explored.append([node.position, node.parent, node.cost, node.action])
                    break

    def f_n(self, parent, position, goal_position):
        global costt
        costt = 0
        for node in frontier:
            if node.position == parent:
                costt = node.cost
        g_n = 1 + costt
        h_n = (abs(goal_position[0] - position[0])) + (abs(goal_position[1] - position[1]))
        return g_n + h_n

    def solution(self, pos):
        goal_pos, goal_cost = self.expand(pos)
        for ex in explored:
            if ex.position == goal_pos:
                path.index(0, ex.action)
                goal_pos = ex.parent
        return path, goal_cost
