from base import BaseAgent, TurnData, Action, AgentData
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


class Agent(BaseAgent):

    def do_turn(self, turn_data: TurnData) -> Action:
        global turn_counter, diamond_pos, bases_pos, result, bases_cost, diamond_pos_4

        # ------------------------------------------ PHASE 4 ------------------------------------------
        if turn_counter == 0:
            for map_row in range(self.grid_size):
                for map_column in range(self.grid_size):
                    if re.match(r'\d', turn_data.map[map_row][map_column]):
                        if turn_data.map[map_row][map_column] == 0:
                            diamond_pos_4[0].append((map_row, map_column))
                        elif turn_data.map[map_row][map_column] == 1:
                            diamond_pos_4[1].append((map_row, map_column))
                        elif turn_data.map[map_row][map_column] == 3:
                            diamond_pos_4[2].append((map_row, map_column))
                        elif turn_data.map[map_row][map_column] == 4:
                            diamond_pos_4[3].append((map_row, map_column))
                        else:
                            diamond_pos_4[4].append((map_row, map_column))
                    elif re.match(r'a', turn_data.map[map_row][map_column]):
                        bases_pos.append((map_row, map_column))
            turn_counter += 1

            sequence = Minimax_algorithm(diamond_pos_4, AgentData.count_required, len(turn_data.agent_data))

            for agent in turn_data.agent_data:
                origin_pos = agent.position
                while sequence.answer:
                    for diamond in sequence.answer:
                        algorithm = A_star(self.grid_size, origin_pos, diamond, turn_data.map)
                        d_path, d_cost = algorithm.solution(origin_pos)
                        for base in bases_pos:
                            algorithm = A_star(self.grid_size, d_path, base, turn_data.map)
                            b_path, b_cost = algorithm.solution(d_path)
                            bases_cost[base] = [b_path, b_cost]
                        min_base = min(bases_cost.keys(), key=lambda t: bases_cost[t][1])
                        min_b_path = bases_cost[min_base][0]
                        origin_pos = min_base
                        result.extend(t for t in d_path)
                        result.extend(t for t in min_b_path)
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

        print(result)
        current_act = result.pop(0)
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
