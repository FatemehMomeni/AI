from copy import deepcopy
from typing import Dict, Any

tree_container: Dict[Any, Any] = dict()
child_list = list()


class Minimax_tree:

    def __init__(self, id, unique, turn: int, agent_num, utility, collect):
        # collect: collected diamond for each agent
        self.agent_num = agent_num
        self.id = id
        self.unique = unique
        self.turn = turn
        self.utility = utility
        self.agents_collected = [[] for _ in range(self.agent_num)]
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
    def search_collected_utility(unique):
        for obj in tree_container.values():
            for v in obj:
                if v.unique == unique:
                    return v.agents_collected, v.utility, v.turn
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
    unique = 1

    current = list()

    def __init__(self, diamonds: list, min_required: dict):
        self.min_required = min_required
        self.agent_num = len(list(self.min_required))
        self.second_constraint = list()
        p = [[] for _ in range(self.agent_num)]
        self.second_constraint.extend(p)
        self.answer = self.minimax(0, diamonds, 0)

    def minimax(self, turn: int, current_diamonds: list, par_unique: int):
        # parent_turn and par_unique belongs to agent who has moved
        # turn belongs to agent who is going to move

        for diamond in current_diamonds:
            won = False
            if par_unique == 0:
                collected = [[] for _ in range(self.agent_num)]
                utility = [0 for _ in range(self.agent_num)]
                parent_turn = 0
            else:
                collected, utility, parent_turn = Minimax_tree.search_collected_utility(par_unique)
            my_collected = deepcopy(collected)
            my_utility = deepcopy(utility)
            my_collected[parent_turn].append(diamond)

            if diamond[1] in self.second_constraint[parent_turn]:
                self.second_constraint[parent_turn].clear()
            else:
                if len(self.second_constraint[parent_turn]) == 4:
                    won = True
            self.second_constraint[parent_turn].append(diamond[1])

            mine = 0
            for agent in my_collected:
                for dia in agent:
                    if dia[1] == diamond[1]:
                        mine += 1
            if not won:
                if mine >= self.min_required[parent_turn][diamond[1]]:
                    my_utility[parent_turn] += self.diamond_scores[diamond[1]]
            else:
                my_utility[parent_turn] += 100

            locals()
            self.current = deepcopy(current_diamonds)
            for agent in my_collected:
                for dia in agent:
                    if dia in self.current:
                        self.current.remove(dia)

            if parent_turn != self.agent_num - 1:
                turn = parent_turn + 1
            else:
                turn = 0

            node = Minimax_tree(diamond[0], self.unique, turn, self.agent_num, my_utility, my_collected)
            tree_container.setdefault(par_unique, []).append(node)
            child_list.append((self.unique, self.current))
            self.unique += 1

        if child_list:
            child = child_list.pop(0)
            self.minimax(turn, child[1], child[0])

        if par_unique == 0:
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
