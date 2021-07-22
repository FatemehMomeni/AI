import random
from copy import deepcopy
from typing import Dict, Any

tree_container: Dict[Any, Any] = dict()


class Minimax_tree:

    def __init__(self, id, parent_id, unique, turn: int, agent_num, utility, collect):
        # collect: collected diamond for each agent
        self.agent_num = agent_num
        self.id = id
        self.parent_id = parent_id
        self.unique = unique
        self.turn = turn
        self.utility = utility
        self.agents_collected = [{0: [], 1: [], 2: [], 3: [], 4: []} for _ in range(self.agent_num)]
        for arg in range(len(collect)):
            self.agents_collected[arg] = collect[arg]

    @staticmethod
    def search_unique(id, parent_id, turn):
        for obj in tree_container.values():
            for v in obj:
                if v.id == id and v.parent_id == parent_id and v.turn == turn:
                    return v.unique
        return None

    @staticmethod
    def search_collected_utility(id, parent_id, turn):
        for obj in tree_container.values():
            for v in obj:
                if v.id == id and v.parent_id == parent_id and v.turn == turn:
                    return v.agents_collected, v.utility
        return None

    @staticmethod
    def search_turn(id):
        for obj in tree_container.values():
            for v in obj:
                if v.unique == id:
                    return v.turn
        return None

    @staticmethod
    def search_pos(id):
        for obj in tree_container.values():
            for v in obj:
                if v.unique == id:
                    return v.id
        return None

    @staticmethod
    def update_utility(id, utility: list):
        for obj in tree_container.values():
            for v in obj:
                if v.unique == id:
                    v.utility = utility


class Minimax_algorithm:
    diamond_scores = [2, 5, 3, 1, 10]  # green, blue, red, yellow, gray
    unique = 0

    def __init__(self, diamonds: dict, min_required: dict, pos_A):
        self.diamond_num = list()
        self.utility = list()
        self.collected: dict[any, any] = dict()
        self.min_required = min_required
        self.agent_num = len(list(self.min_required))
        self.diamonds = diamonds
        p = [len(self.diamonds[d]) for d in self.diamonds]
        self.diamond_num.extend(p)  # number of each color diamond
        self.answer = self.minimax(pos_A, (-1, -1), 0, self.diamonds)

    def minimax(self, position: tuple, parent: tuple, turn: int, current_diamonds: dict):
        pos = par = tuple()
        children_pos = list()
        real_collected = dict()
        real_utility = list()

        for color in range(len(self.diamond_num)):
            par_unique = 0
            if turn != 0:
                par_turn = turn - 1
            else:
                par_turn = self.agent_num - 1
            if parent == (-1, -1):
                self.collected = [{0: [], 1: [], 2: [], 3: [], 4: []} for _ in range(self.agent_num)]
                self.utility = [0 for _ in range(self.agent_num)]
                #tree_container[((-1, -1), -1)] = [Minimax_tree(position, (-1, -1), self.unique, turn,
                                                               #self.agent_num, self.utility, self.collected)]
            elif color == 0:
                self.collected, self.utility = Minimax_tree.search_collected_utility(position, parent, par_turn)
                real_collected = deepcopy(self.collected)
                real_utility = deepcopy(self.utility)
            else:
                self.collected = deepcopy(real_collected)
                self.utility = deepcopy(real_utility)
            if len(current_diamonds[color]) != 0:
                if parent != (-1, -1):
                    par_unique = Minimax_tree.search_unique(position, parent, par_turn)
                color_num = random.randint(0, len(current_diamonds[color])-1)
                self.collected[turn][color].append(current_diamonds[color][color_num])
                if len(self.collected[turn][color]) >= self.min_required[turn][color]:
                    self.utility[turn] += self.diamond_scores[color]
                locals()
                current = {0: [], 1: [], 2: [], 3: [], 4: []}
                for k, v in current_diamonds.items():
                    if v:
                        for i in range(len(v)):
                            not_selected = True
                            for c in range(self.agent_num):
                                if v[i] in self.collected[c][k]:
                                    not_selected = False
                                    break
                            if not_selected:
                                current[k].append(v[i])

                pos = current_diamonds[color][color_num]
                children_pos.extend([[pos, current]])
                par = position

                """print('pos', pos, 'par', par, 'collected', self.collected, 'unique', self.unique, 'par_unique', par_unique,
                      'utility', self.utility, 'turn', turn, '\n---------------------------------------------------')"""

                self.unique += 1
                node = Minimax_tree(pos, par, self.unique, turn, self.agent_num, self.utility, self.collected)
                tree_container.setdefault(par_unique, []).append(node)

        if turn % self.agent_num == self.agent_num - 1:
            turn = 0
        else:
            turn += 1
        for c in children_pos:
            self.minimax(c[0], par, turn, c[1])

        if parent == (-1, -1):
            return self.sequence()
        return

    def sequence(self):
        self.find_best_child(0, tree_container.get(0))
        sequence = list()
        path = 0
        while path in tree_container:
            sequence.append(tree_container[path][0].unique)
            path = tree_container[path][0].unique

        for i in range(len(sequence)):
            sequence[i] = Minimax_tree.search_pos(sequence[i])

        return sequence

    def find_best_child(self, parent: int, children: list):
        max_list = dict()
        maximum = 0
        utility = list()
        for child in children:
            if child.unique in tree_container:
                self.find_best_child(child.unique, tree_container[child.unique])
            utility_vector = child.utility
            if parent:
                turn = Minimax_tree.search_turn(parent)
                if turn != self.agent_num - 1:
                    turn += 1
                else:
                    turn = 0
            else:
                turn = 0
            if utility_vector[turn] > maximum:
                locals()
                maximum = utility_vector[turn]
                max_list.clear()
                max_list[parent] = [child]
                utility = utility_vector

        Minimax_tree.update_utility(parent, utility)
        tree_container.update(max_list)
