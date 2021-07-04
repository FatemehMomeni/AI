import random


agent_num = 0


class Minimax_tree:
    agent_num = agent_num  # this variable contains number of agents
    class_objects = list()

    def __init__(self, utility_vector: list, id, parent_id, level: int, remain_diamond: list, *args):
        # *args: collected diamond for each agent
        self.utility_vector = utility_vector
        self.id = id
        self.parent_id = parent_id
        self.level = level
        self.remain_diamond = remain_diamond
        agents_collected = [[] for i in range(self.agent_num)]
        for arg in range(len(args)):
            agents_collected[arg].append(args[arg])

    @staticmethod
    def search(id):
        for obj in Minimax_tree.class_objects:
            if obj.id == id:
                return obj.utility_vector, obj.remain_diamond, obj.agents_collected
        return None

    @staticmethod
    def search_util_level(id):
        for obj in Minimax_tree.class_objects:
            if obj.id == id:
                return obj.utility_vector, obj.level
        return None

    @staticmethod
    def search_parent(id):
        for obj in Minimax_tree.class_objects:
            if obj.id == id:
                return obj.parent_id
        return None


class Minimax_algorithm:
    diamond_scores = [2, 5, 3, 1, 10]  # green, blue, red, yellow, gray
    min_diamonds = list()
    utility = list()
    remained = list()
    collected = list()
    stop = False

    def __init__(self, diamonds: dict, min_diamonds: list, agents):
        global agent_num
        agent_num = agents

        self.diamond_num = list()
        self.diamonds = diamonds
        self.diamond_num.append(len(self.diamonds[d]) for d in self.diamonds)  # number of each color diamond
        self.min_diamonds = min_diamonds
        self.answer = self.minimax((-1, -1), (-1, -1), 0)

    def minimax(self, position: tuple, parent: tuple, level: int):
        self.utility.clear()
        self.remained.clear()
        self.collected.clear()
        pos = tuple()
        par = tuple()
        if parent == (-1, -1):
            for n in range(Minimax_tree.agent_num):
                self.utility.append(0)
            self.remained = self.diamond_num
            self.collected = [[] for i in range(Minimax_tree.agent_num)]
            pos = position
            par = parent
        for color in range(len(self.diamond_num)):
            if parent != (-1, -1):
                self.utility, self.remained, self.collected = Minimax_tree.search(parent)
            if self.remained[color] != 0 and self.remained[color] >= self.min_diamonds[level]:
                if self.collected[level].count(color) > self.min_diamonds[level][color] or self.collected[level]\
                        .count(color) + 1 == self.min_diamonds[level][color]:
                    choose_color = 0
                    if self.diamonds[color] > 1:
                        choose_color = random.random(0, len(self.diamonds[color]))
                    self.utility[level] += self.diamond_scores[color]
                    self.remained[color] -= 1
                    par = position
                    pos = self.diamonds[color][choose_color]
                    self.diamonds[color].pop(choose_color)
                    self.collected[level].append(color)
            else:
                self.stop = True
        if not self.stop:
            if level % Minimax_tree.agent_num == 3:
                level = 0
            else:
                level = level + 1
            node = Minimax_tree(self.utility, pos, par, level, self.remained, self.collected)
            Minimax_tree.class_objects.append(node)
            self.minimax(pos, par, level)

        if par == pos == (-1, -1):
            return self.sequence()

        return

    def sequence(self):
        parent_children = dict()
        for obj in Minimax_tree.class_objects:
            if parent_children[obj.parent_id] not in parent_children and parent_children[obj.parent_id] is not None:
                parent_children[obj.parent_id] = [parent_children[obj.id]]
            else:
                parent_children[obj.parent_id].append(parent_children[obj.id])

        self.find_best_child(parent_children, list(parent_children.values())[0])

        sequence = list()  # last element of this list is root of the found path, so it should be parsed from end
        sequence.append(list(parent_children.values())[0][1])
        end_sequence = False
        while not end_sequence:
            node = Minimax_tree.search_parent(sequence[len(sequence) - 1])
            sequence.append(node)
            if node is None:
                end_sequence = True

        sequence.reverse()
        return sequence

    def find_best_child(self, parent_children, children):
        max_list = dict()
        for child in children:
            max_list.clear()
            maximum = 0
            if child in parent_children:
                self.find_best_child(parent_children, parent_children[child])
            else:
                utility_vector, level = Minimax_tree.search_util_level(child)
                parent = Minimax_tree.search_parent(child)
                if utility_vector[level] > maximum:
                    locals()
                    maximum = utility_vector[level]
                    max_list.clear()
                    max_list[parent] = [utility_vector, child]
        parent_children.update(max_list)
