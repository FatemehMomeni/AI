import random
<<<<<<< HEAD
from copy import deepcopy
=======
>>>>>>> 8db88630c58ec3a5d8744d57923335e0888d1050
from typing import Dict, Any

tree_container: Dict[Any, Any] = dict()


class Minimax_tree:

<<<<<<< HEAD
    def __init__(self, id, parent_id, turn: int, agent_num, utility, collect):
        # collect: collected diamond for each agent
=======
    def __init__(self, id, parent_id, turn: int, remain_diamond: dict, agent_num, utility, *args):
        # *args: collected diamond for each agent
>>>>>>> 8db88630c58ec3a5d8744d57923335e0888d1050
        self.agent_num = agent_num
        self.id = id
        self.parent_id = parent_id
        self.turn = turn
        self.utility = utility
<<<<<<< HEAD
        self.agents_collected = [[] for _ in range(self.agent_num)]
        for arg in range(len(collect)):
            self.agents_collected[arg].extend(collect[arg])

    @staticmethod
    def search(id, parent_id, turn):
        for obj in tree_container.values():
            for v in obj:
                if v.id == id and v.parent_id == parent_id and v.turn == turn:
                    return v.utility
        return None

    @staticmethod
    def search_collected(id, parent_id, turn):
        for obj in tree_container.values():
            for v in obj:
                if v.id == id and v.parent_id == parent_id and v.turn == turn:
                    return v.agents_collected
        return None

    @staticmethod
    def search_util_turn(id, parent_id):
        for obj in tree_container.values():
            for v in obj:
                if v.id == id and v.parent_id == parent_id:
                    return v.utility, v.turn
=======
        self.remain_diamond = remain_diamond
        agents_collected = [[] for _ in range(self.agent_num)]
        for arg in range(len(args)):
            for i in args[arg]:
                agents_collected[arg].extend(i)

    @staticmethod
    def search(id):
        for obj in tree_container.values():
            for v in obj:
                if v.id == id:
                    return v.utility_vector, v.remain_diamond, v.agents_collected
        return None

    @staticmethod
    def search_remained(id):
        for obj in tree_container.values():
            for v in obj:
                if v.id == id:
                    return v.remain_diamond
        return None

    @staticmethod
    def search_util_turn(id):
        for obj in tree_container.values():
            for v in obj:
                if v.id == id:
                    return v.utility_vector, v.turn
>>>>>>> 8db88630c58ec3a5d8744d57923335e0888d1050
        return None

    @staticmethod
    def search_parent(id):
        for obj in tree_container.values():
            for v in obj:
                if v.id == id:
                    return v.parent_id
        return None


class Minimax_algorithm:
    diamond_scores = [2, 5, 3, 1, 10]  # green, blue, red, yellow, gray
<<<<<<< HEAD

    def __init__(self, diamonds: dict, min_required: dict, pos_A):
        self.diamond_num = list()
        self.utility = list()
        self.collected: list[any, any] = list()
=======
    stop = False

    def __init__(self, diamonds: dict, min_required: dict, pos_A):
        self.remained = dict()
        self.diamond_num = list()
        self.utility = list()
        self.collected: list[any, any] = list()

        self.level_tree = -1
>>>>>>> 8db88630c58ec3a5d8744d57923335e0888d1050
        self.min_required = min_required
        self.agent_num = len(list(self.min_required))
        self.diamonds = diamonds
        p = [len(self.diamonds[d]) for d in self.diamonds]
        self.diamond_num.extend(p)  # number of each color diamond
<<<<<<< HEAD
        self.answer = self.minimax(pos_A, (-1, -1), 0, self.diamonds)

    def minimax(self, position: tuple, parent: tuple, turn: int, current_diamonds: dict):
        pos = par = tuple()
        children_pos = list()
        real_collected = list()

        for color in range(len(self.diamond_num)):
            if parent == (-1, -1):
                self.collected = [[] for _ in range(self.agent_num)]
                self.utility = [0 for _ in range(self.agent_num)]
                tree_container[(-1, -1)] = [Minimax_tree(position, (-1, -1), turn, self.agent_num,
                                                         self.utility, self.collected)]
            elif color == 0:
                self.collected = Minimax_tree.search_collected(position, parent, not turn)
                real_collected = deepcopy(self.collected)
            else:
                self.collected = deepcopy(real_collected)
            if len(current_diamonds[color]) != 0:
                if parent != (-1, -1):
                    self.utility = Minimax_tree.search(position, parent, not turn)
                color_num = random.randint(0, len(current_diamonds[color])-1)
                self.collected[turn].append(current_diamonds[color][color_num])
                locals()
                current = dict()
                for k, v in current_diamonds.items():
                    if v:
                        for i in range(len(v)):
                            flag = True
                            for c in self.collected:
                                if v[i] in c:
                                    flag = False
                                    break
                            if flag:
                                current.setdefault(k, []).append(v[i])
                            else:
                                current.setdefault(k, [])
                    else:
                        current.setdefault(k, [])
                pos = current_diamonds[color][color_num]
                children_pos.extend([[pos, current]])
                par = position
                if self.collected[turn].count(color) >= self.min_required[turn][color]:
                    self.utility[turn] += self.diamond_scores[color]
                node = Minimax_tree(pos, par, turn, self.agent_num, self.utility, self.collected)
                tree_container.setdefault(par, []).append(node)

        if turn % self.agent_num == self.agent_num - 1:
            turn = 0
        else:
            turn += 1
        for c in children_pos:
            self.minimax(c[0], par, turn, c[1])
=======
        self.answer = self.minimax(pos_A, (-1, -1), 0)

    def minimax(self, position: tuple, parent: tuple, turn: int):
        pos = par = tuple()
        children_pos = list(tuple())

        for color in range(len(self.diamond_num)):
            if self.diamond_num[color] != 0:
                if parent == (-1, -1):
                    self.remained = self.diamonds.copy()
                    self.collected = [[] for _ in range(self.agent_num)]
                    self.utility = [0 for _ in range(self.agent_num)]
                    tree_container[(-1, -1)] = [Minimax_tree(position, (-1, -1), turn, self.remained, self.agent_num, self.utility, self.collected)]
                else:
                    self.utility, self.remained, self.collected = Minimax_tree.search(parent)
                color_num = random.randint(0, self.diamond_num[color] - 1)
                self.collected[turn].append(color)
                self.diamond_num[color] -= 1
                locals()
                pos = self.diamonds[color][color_num]
                children_pos.append(pos)
                par = position
                if self.collected[turn].count(color) >= self.min_required[turn][color]:
                    self.utility[turn] += self.diamond_scores[color]
                self.diamonds[color].pop(color_num)
                node = Minimax_tree(pos, par, turn, self.remained, self.agent_num, self.utility, self.collected)
                tree_container.setdefault(par, []).append(node)
        for c in children_pos:
            """tree_container = {dict: 2} {(-1, -1): [<adversarial.Minimax_tree object at 0x0000020B202FE8E0>], (6, 3): [<adversarial.Minimax_tree object at 0x0000020B20286880>, <adversarial.Minimax_tree object at 0x0000020B202D7040>, <adversarial.Minimax_tree object at 0x0000020B20283AF0>]}if turn % self.agent_num == self.agent_num - 1:
                turn = 0
            else:
                turn = turn + 1"""
            self.level_tree += 1
            turn = self.level_tree % self.agent_num
            parent_remained = Minimax_tree.search_remained(parent)
            print(self.diamond_num)
            for k in parent_remained.keys():
                self.diamond_num[k] = len(parent_remained[k])

            print(self.diamond_num)
            self.minimax(c, par, turn)
>>>>>>> 8db88630c58ec3a5d8744d57923335e0888d1050

        if parent == (-1, -1):
            return self.sequence()
        return

    def sequence(self):
<<<<<<< HEAD
        self.find_best_child(tree_container.get((-1, -1)))
        sequence = list()  # last element of this list is root of the found path, so it should be parsed from end
        print(tree_container)
        #print('sequence', sequence)
=======

        self.find_best_child(tree_container.get((-1, -1)))
        sequence = list()  # last element of this list is root of the found path, so it should be parsed from end
>>>>>>> 8db88630c58ec3a5d8744d57923335e0888d1050
        sequence.append(list(tree_container.values())[0][1])
        end_sequence = False
        while not end_sequence:
            node = Minimax_tree.search_parent(sequence[0])
            sequence.insert(0, node)
            if node is None:
                end_sequence = True
        return sequence

    def find_best_child(self, children: list):
        max_list = dict()
        for child in children:
            max_list.clear()
            maximum = 0
            if child in tree_container:
                self.find_best_child(tree_container[child])
            else:
<<<<<<< HEAD
                utility_vector, turn = Minimax_tree.search_util_turn(child.id, child.parent_id)
=======
                utility_vector, turn = Minimax_tree.search_util_turn(child.id)
>>>>>>> 8db88630c58ec3a5d8744d57923335e0888d1050
                parent = Minimax_tree.search_parent(child.id)
                if utility_vector[turn] > maximum:
                    locals()
                    maximum = utility_vector[turn]
                    max_list.clear()
                    max_list[parent] = [utility_vector, child]

        tree_container.update(max_list)
