"""class Node:

    def __init__(self, position, parent, cost, action):
        self.position = position
        self.parent = parent
        self.cost = cost
        self.action = action
"""
from typing import Dict, Any

explored: Dict[Any, Any] = dict()
path = list()
dest_pos = tuple()
dest_cost = -1


class A_star:

    def __init__(self, grid_size, position, goal_position, mapp):
        self.grid_size = grid_size
        self.position = self.agent_pos = position
        self.destination = goal_position
        self.map = mapp
        self.frontier : Dict[Any, Any] = dict()
        explored.clear()
        path.clear()
        self.first_time = True
        self.minimum = 0
        self.min_index = 0
        self.first_time_expand = True
        self.first_add_to_frontier = True

    def expand(self, pos):
        #print("in expand...")
        flag = True
        frontier_index = 0
        add_frontier_index = 0
        cost_parent = -1

        actions = {"UP": (pos[0]-1, pos[1]), "DOWN": (pos[0]+1, pos[1]),
                   "LEFT": (pos[0], pos[1]-1), "RIGHT": (pos[0], pos[1]+1)}

        if self.first_time:
            price = self.f_n(None, 0, pos, self.destination)
            #frontier.append([pos, None, price, None])
            self.frontier.update({pos :[pos,None, price, None]})
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
                        #for ex_node in range(len(explored)):
                        for ex_pos in explored:
                            #if explored[ex_node][0] == pos:
                            if ex_pos == pos:
                                #cost_parent = explored[ex_node][2]
                                cost_parent = explored.get(ex_pos)[2]
                            #if actions[act_key] == explored[ex_node][0]:
                            if actions[act_key] == explored.get(ex_pos)[0]:
                                explored_flag = True
                        if not explored_flag:
                            price = self.f_n(pos, cost_parent, actions[act_key], self.destination)
                            #for node in range(len(frontier)):
                            for f_pos in self.frontier:
                                """if min_index == 0:
                                    minimum = frontier[node][2]
                                    min_index = 1"""
                                #if frontier[node][0] == actions[act_key] and frontier[node][2] > price:
                                if f_pos == actions.get(act_key) and self.frontier.get(f_pos)[2] > price:
                                    """frontier[node][2] = price
                                    frontier[node][1] = pos
                                    frontier[node][3] = act_key"""
                                    self.frontier.get(f_pos)[2] = price
                                    self.frontier.get(f_pos)[1] = pos
                                    self.frontier.get(f_pos)[3] = act_key
                                    flag = False
                                    break
                            """if flag:
                                if frontier:
                                    while True:
                                        pos_list = list(frontier)
                                        if frontier.get(pos_list[add_frontier_index])[2] < price:
                                            add_frontier_index += 1
                                        elif frontier.get(pos_list[add_frontier_index])[2] >= price:
                                            frontier = dict(sorted(frontier.items(), key=lambda e: e[1][2]))
                                        elif add_frontier_index == len(pos_list):
                                            frontier.update({actions[act_key]: [actions[act_key], pos, price, act_key]})
                                else:
                                    frontier.update({actions[act_key]: [actions[act_key], pos, price, act_key]})"""
                            if flag:
                                self.frontier.update({actions[act_key]: [actions[act_key], pos, price, act_key]})

        self.frontier = dict(sorted(self.frontier.items(), key=lambda e: e[1][2]))
        """pos_list = list(frontier)
        self.minimum = frontier.get(pos_list[0])[2]
        pos_list = list(frontier)
        if self.min_index == 0:
            self.minimum = frontier.get(pos_list[0])[2]
            self.min_index = 1
       # for node in range(len(frontier)):
        for f in frontier:
            #if frontier[node][2] < self.minimum:
            if frontier.get(f)[2] < self.minimum and self.find_dict(explored,frontier.get(f)[1]):
                #self.minimum = frontier[node][2]
                self.minimum = frontier[f][2]"""
        pos_list = list(self.frontier)
        self.minimum = self.frontier.get(pos_list[0])[2]
        print("befor while...")
        while True:
            #print("in while...")
            pos_list = list(self.frontier)
            #print(self.destination)
            print("frontier" ,self.frontier)
            print("explored" , explored)
            print(frontier_index)
            #if frontier[frontier_index][2] == self.minimum and explored :
            #if self.frontier.get(pos_list[frontier_index])[2] == self.minimum :
            if self.first_time_expand:
                val = self.frontier.get(pos_list[frontier_index])
                explored.update({pos_list[frontier_index]: [val[0], val[1], val[2], val[3]]})
                self.frontier.pop(pos_list[frontier_index])
                self.first_time_expand = False
                self.expand(list(explored)[-1])
                break
            #if explored[-1][0] == frontier[frontier_index][1]:
            elif explored.get(list(explored)[-1])[1] != self.frontier.get(pos_list[frontier_index])[1]:
                val = self.frontier.get(pos_list[frontier_index])
                explored.update({pos_list[frontier_index]: [val[0], val[1], val[2], val[3]]})
                self.frontier.pop(pos_list[frontier_index])
                #if frontier[frontier_index][0] == self.destination:
                if val[0] == self.destination:
                    global dest_pos, dest_cost
                    dest_pos, dest_cost = pos_list[frontier_index], val[2]
                    #explored.append(frontier[frontier_index])
                    break
                else:
                    #explored.append(frontier[frontier_index])
                    #self.expand(explored[len(explored)-1][0])
                    #print("second in expand...")
                    self.expand(list(explored)[-1])
                    break
            #frontier_index += 1


    def f_n(self, parent, parent_cost, position, goal_position):

        if not parent:
            g_n = 0
        else:
            parent_hn = (abs(goal_position[0] - parent[0])) + (abs(goal_position[1] - parent[1]))
            g_n = (parent_cost - parent_hn) + 1
        h_n = (abs(goal_position[0] - position[0])) + (abs(goal_position[1] - position[1]))
        return g_n + h_n

    def solution(self, pos):
        #print("start....")
        global dest_pos, dest_cost
        self.expand(pos)
        """key = list(explored)[:0:-1]
        if explored.get(list(explored)[-1])[0] == dest_pos:
            dest = list(explored)[-1]
            for k in key:
                path.append(explored.get(dest)[3])
                dest = explored.get(k)[1]"""
        key = list(explored)[1:]
        dest = list(explored)[-1]
        for k in key:
            print(dest)
            if not explored.get(dest)[3]:
                break
            #path.append(explored.get(k)[3])
            path.append(explored.get(dest)[3])
            dest = explored.get(dest)[1]
        print("khar")
        """key = list(explored)[1:]
        for k in key:
            path.append(explored.get(k)[3])"""
        """while dest_pos :
            #print("in while...")
            key = list(explored)[1:]
            for k in key:
                if explored[k][0] == dest_pos:
                    path.insert(0, explored[k][3])
                    dest_pos = explored[k][1]"""
        return list(reversed(path)), dest_cost

    def find_dict(self,Dict,parent):
        d_list = list(Dict)
        for d in d_list:
            if Dict.get(d)[1] == parent:return True
            else:return False

