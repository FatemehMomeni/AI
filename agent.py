import operator
from base import BaseAgent, TurnData, Action
from tree import A_star
import re


turn_counter = 0
diamond_pos = list(tuple())
bases_pos = list(tuple())
bases_cost = list(tuple())
result = list()


class Agent(BaseAgent):

    def do_turn(self, turn_data: TurnData) -> Action:
        global turn_counter, diamond_pos, bases_pos, result, bases_cost

        if turn_counter == 0:
            for map_row in range(self.grid_size):
                for map_column in range(self.grid_size):
                    if re.match(r'\d', turn_data.map[map_row][map_column]):
                        diamond_pos.append((map_row, map_column))
                    elif re.match(r'[a-z]', turn_data.map[map_row][map_column]):
                        bases_pos.append((map_row, map_column))
            turn_counter += 1

            for agent in turn_data.agent_data:
                for diamond in range(len(diamond_pos)):
                    algorithm = A_star(self.grid_size, agent.position, diamond_pos[diamond], turn_data.map)
                    path, cost = algorithm.solution(agent.position)
                    result = path

            for agent in turn_data.agent_data:
                for base in range(len(bases_pos)):
                    algorithm = A_star(self.grid_size, agent.position, bases_pos[base], turn_data.map)
                    path, cost = algorithm.solution(agent.position)
                    bases_cost.append([path, cost])
            min_path = min(bases_cost, key=lambda t: t[1])
            result.append(min_path[0])

        current_act = result.pop(0)
        return current_act


if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)
