from base import BaseAgent, TurnData, Action
from tree import A_star
from adversarial import Minimax_algorithm
import re
from collections import defaultdict

turn_counter = 0
diamond_pos = list(tuple())
diamond_cost = defaultdict(list)
bases_pos = list(tuple())
bases_cost = defaultdict(list)
result = list()

# PHASE 4
diamond_pos_4 = {0: [], 1: [], 2: [], 3: [], 4: []}
bases_pos_4 = {'a': [], 'b': [], 'c': [], 'd': []}
required = dict()
result_4 = list()
pos_A = tuple()


class Agent(BaseAgent):

    def do_turn(self, turn_data: TurnData) -> Action:
        global turn_counter, diamond_pos_4, bases_pos_4, result_4, required, pos_A

        # ------------------------------------------ PHASE 4 ------------------------------------------
        if turn_counter == 0:  # first time
            for map_row in range(self.grid_size):
                for map_column in range(self.grid_size):
                    if re.match(r'\d', turn_data.map[map_row][map_column]):
                        if turn_data.map[map_row][map_column] == '0':
                            diamond_pos_4.setdefault(0, []).append((map_row, map_column))
                        elif turn_data.map[map_row][map_column] == '1':
                            diamond_pos_4.setdefault(1, []).append((map_row, map_column))
                        elif turn_data.map[map_row][map_column] == '2':
                            diamond_pos_4.setdefault(2, []).append((map_row, map_column))
                        elif turn_data.map[map_row][map_column] == '3':
                            diamond_pos_4.setdefault(3, []).append((map_row, map_column))
                        else:
                            diamond_pos_4.setdefault(4, []).append((map_row, map_column))
                    elif re.match(r'[a-d]', turn_data.map[map_row][map_column]):
                        if turn_data.map[map_row][map_column] == 'a':
                            bases_pos_4.setdefault('a', []).append((map_row, map_column))
                        elif turn_data.map[map_row][map_column] == 'b':
                            bases_pos_4.setdefault('b', []).append((map_row, map_column))
                        elif turn_data.map[map_row][map_column] == 'c':
                            bases_pos_4.setdefault('c', []).append((map_row, map_column))
                        else:
                            bases_pos_4.setdefault('d', []).append((map_row, map_column))
            turn_counter += 1

            for agent in range(len(turn_data.agent_data)):
                if agent == 0:
                    required.setdefault(0, []).extend(turn_data.agent_data[agent].count_required)
                    pos_A = turn_data.agent_data[agent].position
                elif agent == 1:
                    required.setdefault(1, []).extend(turn_data.agent_data[agent].count_required)
                elif agent == 2:
                    required.setdefault(2, []).extend(turn_data.agent_data[agent].count_required)
                else:
                    required.setdefault(3, []).extend(turn_data.agent_data[agent].count_required)

            sequence = Minimax_algorithm(diamond_pos_4, required, pos_A)

            all_agents = len(turn_data.agent_data)
            agent_num = 0
            for i in range(len(turn_data.agent_data)):
                if turn_data.agent_data[i].name == self.name:
                    agent_num = i
                    break

            my_diamonds = list()
            dia_pos = 0
            while agent_num + dia_pos * all_agents < len(sequence.answer):
                my_diamonds.append(sequence.answer[agent_num + dia_pos * all_agents])
                dia_pos += 1

            origin_pos = turn_data.agent_data[agent_num].position
            for diamond in my_diamonds:
                algorithm = A_star(self.grid_size, origin_pos, diamond, turn_data.map)
                d_path, d_cost = algorithm.solution(origin_pos)
                for base in bases_pos:
                    algorithm = A_star(self.grid_size, d_path, base, turn_data.map)
                    b_path, b_cost = algorithm.solution(d_path)
                    bases_cost[base] = [b_path, b_cost]
                min_base = min(bases_cost.keys(), key=lambda t: bases_cost[t][1])
                min_b_path = bases_cost[min_base][0]
                origin_pos = min_base
                result_4.extend(t for t in d_path)
                result_4.extend(t for t in min_b_path)
                sequence.answer.remove(d_path)
                diamond_cost.clear()
                bases_cost.clear()
        # ------------------------------------------ PHASE 4 ------------------------------------------

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

        print(result_4)
        current_act = result_4.pop(0)

        if current_act == "UP":
            return Action.UP
        elif current_act == "DOWN":
            return Action.DOWN
        elif current_act == "LEFT":
            return Action.LEFT
        elif current_act == "RIGHT":
            return Action.RIGHT
        # return random.choice(list(Action))


if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)
