"""class Node:
    def __init__(self, position, parent, cost, action):
        self.position = position
        self.parent = parent
        self.cost = cost
        self.action = action
"""
from typing import Dict, Any

path = list()
dest_pos = tuple()
dest_cost = -1


class A_star:

    def __init__(self, grid_size, position, goal_position, mapp):
        self.grid_size = grid_size
        self.position = self.agent_pos = position
        self.destination = goal_position
        self.map = mapp
        self.frontier: Dict[Any, Any] = dict()
        self.explored: Dict[Any, Any] = dict()
        path.clear()
        self.first_time = True
        self.minimum = 0
        self.min_index = 0
        self.first_time_expand = True
        self.first_add_to_frontier = True

    def expand(self, pos):
        flag = True
        frontier_index = 0
        cost_parent = -1

        actions = {"UP": (pos[0]-1, pos[1]), "DOWN": (pos[0]+1, pos[1]),
                   "LEFT": (pos[0], pos[1]-1), "RIGHT": (pos[0], pos[1]+1)}

        if self.first_time:
            price = self.f_n(None, 0, pos, self.destination)
            self.frontier.update({pos: [pos, None, price, None]})
            self.first_time = False
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
                        for ex_pos in self.explored:
                            if ex_pos == pos:
                                cost_parent = self.explored.get(ex_pos)[2]
                            if actions[act_key] == self.explored.get(ex_pos)[0]:
                                explored_flag = True
                        if not explored_flag:
                            price = self.f_n(pos, cost_parent, actions[act_key], self.destination)
                            for f_pos in self.frontier:
                                if f_pos == actions.get(act_key) and self.frontier.get(f_pos)[2] > price:
                                    self.frontier.get(f_pos)[2] = price
                                    self.frontier.get(f_pos)[1] = pos
                                    self.frontier.get(f_pos)[3] = act_key
                                    flag = False
                                    break
                            if flag:
                                self.frontier.update({actions[act_key]: [actions[act_key], pos, price, act_key]})

        self.frontier = dict(sorted(self.frontier.items(), key=lambda e: e[1][2]))
        pos_list = list(self.frontier)
        self.minimum = self.frontier.get(pos_list[0])[2]
        while True:
            if self.first_time_expand:
                val = self.frontier.get(pos_list[frontier_index])
                self.explored.update({pos_list[frontier_index]: [val[0], val[1], val[2], val[3]]})
                self.frontier.pop(pos_list[frontier_index])
                self.first_time_expand = False
                self.expand(list(self.explored)[-1])
                break
            # elif self.explored.get(list(self.explored)[-1])[1] != self.frontier.get(pos_list[frontier_index])[1]:
            else:
                val = self.frontier.get(pos_list[frontier_index])
                self.explored.update({pos_list[frontier_index]: [val[0], val[1], val[2], val[3]]})
                self.frontier.pop(pos_list[frontier_index])
                if val[0] == self.destination:
                    global dest_pos, dest_cost
                    dest_pos, dest_cost = pos_list[0], val[2]
                    break
                else:
                    self.expand(list(self.explored)[-1])
                    break

            # frontier_index += 1

    def f_n(self, parent, parent_cost, position, goal_position):
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
        key = list(self.explored)[1:]
        dest = list(self.explored)[-1]
        for k in key:
            if not self.explored.get(dest)[3]:
                break
            path.append(self.explored.get(dest)[3])
            dest = self.explored.get(dest)[1]
        return list(reversed(path)), dest_cost


