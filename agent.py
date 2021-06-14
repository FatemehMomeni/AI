import operator
import random

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
            for base in range(len(bases_pos)):
                for diamond in range(len(diamond_pos)):
                    algorithm = A_star(self.grid_size,  diamond_pos[diamond], bases_pos[base], turn_data.map)
                    path, cost = algorithm.solution(diamond_pos[diamond])
                    bases_cost.append([path, cost])
            print("lk")
            min_path = min(bases_cost, key=lambda t: t[1])
            result.extend(min_path[0])

        current_act = result.pop(0)
        #print(type(current_act),current_act)
        if current_act == "UP":
            return Action.UP
        elif current_act == "DOWN":
            return Action.DOWN
        elif current_act == "LEFT":
            return Action.LEFT
        elif current_act == "RIGHT":
            return Action.RIGHT
        #return random.choice(list(Action))

if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)
