from base import BaseAgent, TurnData, Action
from tree import A_star
from adversarial import Minimax_algorithm
from collections import defaultdict
from copy import deepcopy
import random
import re

turn_counter = 0
diamond_pos = list(tuple())
diamond_cost = defaultdict(list)
bases_pos = list(tuple())
bases_cost = defaultdict(list)
result = list()

# PHASE 4
diamond_pos_4 = {0: [], 1: [], 2: [], 3: [], 4: []}
bases_pos_4 = {0: [], 1: [], 2: [], 3: []}
required = dict()
result_4 = list()
pos_A = tuple()


class Agent(BaseAgent):

    @staticmethod
    def pos_of_action(pos, act):
        actions = {"UP": (pos[0] - 1, pos[1]), "DOWN": (pos[0] + 1, pos[1]),
                   "LEFT": (pos[0], pos[1] - 1), "RIGHT": (pos[0], pos[1] + 1)}
        return actions[act]

    def random_action(self, act, new_pos, turn_data, others_pos, agent_num):
        while not(0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size and
                  turn_data.map[new_pos[0]][new_pos[1]] != '*' and
                  turn_data.map[new_pos[0]][new_pos[1]] not in others_pos
                  and not re.match(r'\d', turn_data.map[new_pos[0]][new_pos[1]])):
            act = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            new_pos = self.pos_of_action(turn_data.agent_data[agent_num].position, act)
        return act

    def do_turn(self, turn_data: TurnData) -> Action:
        global turn_counter, diamond_pos_4, bases_pos_4, result_4, required, pos_A, bases_pos
        agent_num = 0
        collide = False
        current_collected = list()
        diamond_scores = [2, 5, 3, 1, 10]  # green, blue, red, yellow, gray

        for i in range(len(turn_data.agent_data)):
            if turn_data.agent_data[i].name == self.name:
                agent_num = i
                break

        # ------------------------------------------ PHASE 4 ------------------------------------------
        if turn_counter == 0:  # first time
            for map_row in range(self.grid_size):
                for map_column in range(self.grid_size):
                    if re.match(r'\d', turn_data.map[map_row][map_column]):
                        diamond_pos.append([(map_row, map_column), int(turn_data.map[map_row][map_column])])
                    elif re.match(r'[a-d]', turn_data.map[map_row][map_column]):
                        if turn_data.map[map_row][map_column] == 'a':
                            bases_pos_4.setdefault(0, []).append((map_row, map_column))
                        elif turn_data.map[map_row][map_column] == 'b':
                            bases_pos_4.setdefault(1, []).append((map_row, map_column))
                        elif turn_data.map[map_row][map_column] == 'c':
                            bases_pos_4.setdefault(2, []).append((map_row, map_column))
                        else:
                            bases_pos_4.setdefault(3, []).append((map_row, map_column))
            turn_counter += 1

            for agent in range(len(turn_data.agent_data)):
                if agent == 0:
                    required.setdefault(0, []).extend(turn_data.agent_data[agent].count_required)
                elif agent == 1:
                    required.setdefault(1, []).extend(turn_data.agent_data[agent].count_required)
                elif agent == 2:
                    required.setdefault(2, []).extend(turn_data.agent_data[agent].count_required)
                else:
                    required.setdefault(3, []).extend(turn_data.agent_data[agent].count_required)

            root = (self.grid_size + 1, self.grid_size + 1)

            sequence = Minimax_algorithm(diamond_pos, required)

            all_agents = len(turn_data.agent_data)
            for i in range(len(turn_data.agent_data)):
                if turn_data.agent_data[i].name == self.name:
                    bases_pos = bases_pos_4[i]
                    break

            my_diamonds = list()
            dia_pos = 0
            while agent_num + dia_pos * all_agents < len(sequence.answer):
                my_diamonds.append(sequence.answer[agent_num + dia_pos * all_agents])
                dia_pos += 1
            for m in my_diamonds:
                sequence.answer.remove(m)

            origin_pos = turn_data.agent_data[agent_num].position
            while my_diamonds:
                for diamond in my_diamonds:
                    algorithm = A_star(self.grid_size, origin_pos, diamond, turn_data.map, sequence.answer)
                    d_path, d_cost = algorithm.solution(origin_pos)
                    diamond_cost[diamond] = [d_path, d_cost]
                min_diamond = min(diamond_cost.keys(), key=lambda t: diamond_cost[t][1])
                min_d_path = diamond_cost[min_diamond][0]
                for base in bases_pos:
                    algorithm = A_star(self.grid_size, min_diamond, base, turn_data.map, sequence.answer)
                    b_path, b_cost = algorithm.solution(min_diamond)
                    bases_cost[base] = [b_path, b_cost]
                min_base = min(bases_cost.keys(), key=lambda t: bases_cost[t][1])
                min_b_path = bases_cost[min_base][0]
                origin_pos = min_base
                result_4.extend(t for t in min_d_path)
                result_4.extend(t for t in min_b_path)
                my_diamonds.remove(min_diamond)
                diamond_cost.clear()
                bases_cost.clear()
        # ------------------------------------------ PHASE 4 ------------------------------------------

        # ------------------------------------------ PHASE 2 ------------------------------------------
        """if turn_counter == 0:
            for map_row in range(self.grid_size):
                for map_column in range(self.grid_size):
                    if re.match(r'\d', turn_data.map[map_row][map_column]):
                        diamond_pos.append((map_row, map_column))
                    elif re.match(r'[a-z]', turn_data.map[map_row][map_column]):
                        bases_pos.append((map_row, map_column))
            turn_counter += 1
            for agent in turn_data.agent_data:
                origin_pos = agent.position
                while diamond_pos:
                    for diamond in diamond_pos:
                        algorithm = A_star(self.grid_size, origin_pos, diamond, turn_data.map)
                        d_path, d_cost = algorithm.solution(origin_pos)
                        diamond_cost[diamond] = [d_path, d_cost]
                    min_diamond = min(diamond_cost.keys(), key=lambda t: diamond_cost[t][1])
                    min_d_path = diamond_cost[min_diamond][0]
                    for base in bases_pos:
                        algorithm = A_star(self.grid_size, min_diamond, base, turn_data.map)
                        b_path, b_cost = algorithm.solution(min_diamond)
                        bases_cost[base] = [b_path, b_cost]
                    min_base = min(bases_cost.keys(), key=lambda t: bases_cost[t][1])
                    min_b_path = bases_cost[min_base][0]
                    origin_pos = min_base
                    result.extend(t for t in min_d_path)
                    result.extend(t for t in min_b_path)
                    diamond_pos.remove(min_diamond)
                    diamond_cost.clear()
                    bases_cost.clear()"""
        # ------------------------------------------ PHASE 2 ------------------------------------------
        locals()
        if len(turn_data.agent_data[agent_num].collected) > len(current_collected):
            current_collected = deepcopy(turn_data.agent_data[agent_num].collected)
            current_color = turn_data.agent_data[agent_num].collected[-1]
            if turn_data.agent_data[agent_num].collected.count(current_color) >= \
                    turn_data.agent_data[agent_num].count_required[current_color]:
                turn_data.agent_data[agent_num].score += diamond_scores[current_color]

        others_pos = list()
        for a in range(len(turn_data.agent_data)):
            if a != agent_num:
                others_pos.append(turn_data.agent_data[a].position)
        if result_4:
            current_act = result_4.pop(0)
            new_pos = self.pos_of_action(turn_data.agent_data[agent_num].position, current_act)
            if new_pos in others_pos:
                result_4.insert(0, current_act)
                current_act = self.random_action(current_act, new_pos, turn_data, others_pos, agent_num)
        else:
            current_act = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            new_pos = self.pos_of_action(turn_data.agent_data[agent_num].position, current_act)
            current_act = self.random_action(current_act, new_pos, turn_data, others_pos, agent_num)

        """others_pos = list()
        for a in range(len(turn_data.agent_data)):
            if a != agent_num:
                others_pos.append(turn_data.agent_data[a].position)
        if result_4:
            current_act = result_4.pop(0)
            new_pos = self.pos_of_action(turn_data.agent_data[agent_num].position, current_act)
            if new_pos in others_pos:
                result_4.insert(0, current_act)
                collide = True
        elif not result_4 or collide:
            current_act = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            new_pos = self.pos_of_action(turn_data.agent_data[agent_num].position, current_act)
            while not(0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size and
                      turn_data.map[new_pos[0]][new_pos[1]] != '*' and new_pos not in others_pos
                      and not re.match(r'\d', turn_data.map[new_pos[0]][new_pos[1]])):
                current_act = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
                new_pos = self.pos_of_action(turn_data.agent_data[agent_num].position, current_act)
        else:
            current_act = None"""

        if current_act == "UP":
            return Action.UP
        elif current_act == "DOWN":
            return Action.DOWN
        elif current_act == "LEFT":
            return Action.LEFT
        elif current_act == "RIGHT":
            return Action.RIGHT
        # return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])


if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)
