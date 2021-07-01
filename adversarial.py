from .base import TurnData


class Minimax_tree:
    agent_num = TurnData.turns_left  # this variable contains number of agents; now for instance number of
    # remaining turns had used instead
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
    diamond_scores = [2, 5, 3, 1, 10]
    min_diamonds = list()
    id = 0
    utility = list()
    remained = list()
    collected = list()

    def __init__(self, diamond_num: list, *args):  # *args: min number of diamonds each agent must be collect
        self.diamond_num = diamond_num  # number of each color diamond
        for min_num in args:
            self.min_diamonds.append(min_num)
        self.minimax(0)

    def minimax(self, level: int):
        self.utility.clear()
        self.remained.clear()
        self.collected.clear()
        stop = False
        if self.id == 0:
            id_local = None
            for n in range(Minimax_tree.agent_num):
                self.utility.append(0)
            self.remained = self.diamond_num
            self.collected = [[] for i in range(Minimax_tree.agent_num)]
        else:
            id_local = self.id
            for color in range(len(self.diamond_num)):
                self.utility, self.remained, self.collected = Minimax_tree.search(id_local)
                if self.remained[color] != 0 and self.remained[color] >= self.min_diamonds[level]:
                    if self.collected[level].count(color) > self.min_diamonds[level][color] or self.collected[level]\
                            .count(color) + 1 == self.min_diamonds[level][color]:
                        self.utility[level] += self.diamond_scores[color]
                        self.remained[color] -= 1
                        self.collected[level].append(color)
                else:
                    stop = True
        if not stop:
            self.id += 1
            if level % Minimax_tree.agent_num == 3:
                level = 0
            else:
                level = level + 1
            node = Minimax_tree(self.utility, self.id, id_local, level, self.remained, self.collected)
            Minimax_tree.class_objects.append(node)
            self.minimax(level)

        if not id_local:
            self.sequence()

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
