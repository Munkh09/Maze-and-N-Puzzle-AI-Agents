from collections import deque
import pygame
import time
from tabulate import tabulate
import json
import copy
import heapq


class Node:
    def __init__(self, state, parent, g, h, blank_tile_loc):
        self.state = state
        self.parent = parent
        self.blank_tile_loc = blank_tile_loc
        self.g = g
        self.h = h
        self.f = g + h
        
    def __lt__(self, other):
        """ Python's built-in sorting Method for Min-Heap Comparison """
        return self.f < other.f

""" An N Puzzle AI Agent that uses either BFS or A* to search and find the goal state """
""" A* works on any ratios of 2D grids, but it assumes that there is no duplicate numbers """
""" BFS works on any ratios of 2D grids """
class NPuzzleAiAgent:
    def __init__(self, initial_state, goal_state, initial_blank_tile_loc, algorithm):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.initial_blank_tile_loc = initial_blank_tile_loc
        # run the chosen algorithm 
        if algorithm == "bfs":
            self.bfs()
        elif algorithm == "a_star":
            # prepare a dictionary to optimize the Manhattan heuristic function calculation
            self.goal_state_tile_locations = self.get_goal_state_tile_locations()
            self.a_star()

    def bfs(self):
        """ Does Breadth First Search on the 8 Puzzle """
        # initialize the queue
        queue = deque()
        queue.append((self.initial_state, self.initial_blank_tile_loc))
        
        # initialize visited state storage
        visited_list = {}

        # initialize storage for states' parents
        state_parents = {json.dumps(self.initial_state): None} 

        while queue:
            current_state, blank_tile_location = queue.popleft()

            # visualize the current state
            self.represent_current_state(current_state)

            # check if the current state is the same as the goal state
            goal_reached = self.test_goal(current_state)

            if (goal_reached):
                print("Goal reached!")
                shortest_path = self.reconstruct_path_bfs(current_state, state_parents)
                print(shortest_path)
                print(len(visited_list))
                return 

            next_states = self.generate_successor_bfs((current_state, blank_tile_location), visited_list, state_parents)

            for state in next_states:
                queue.append(state)

            visited_list[json.dumps(current_state)] = True
            

    def a_star(self):
        """ Does A* to reach the goal state """
        # initialize visited state dictionary
        visited = set()

        min_f_heap = []
        # formulate the root state node
        root_state_h = self.compute_h(self.initial_state)
        root_state_node = Node(self.initial_state, parent = None, blank_tile_loc = self.initial_blank_tile_loc, g = 0, h = root_state_h)
        # add the root state node to the min heap
        heapq.heappush(min_f_heap, root_state_node)

        while min_f_heap:
            current_state_node = heapq.heappop(min_f_heap)

            # visualize the current state visit
            self.represent_current_state(current_state_node.state)

            # check if we reached the goal state
            reached_goal_state = self.test_goal(current_state_node.state)
            
            if (reached_goal_state):
                print("Reached Goal State!")
                print(len(visited))
                return
                # return self.reconstruct_path(current_state_node)
            
            # mark the current state as visited
            current_state = json.dumps(current_state_node.state)
            if (current_state not in visited):
                visited.add(current_state)
                # assign and retrieve successor nodes
                next_state_nodes = self.generate_successor(current_state_node)
                for state_node in next_state_nodes:
                    heapq.heappush(min_f_heap, state_node)
        
        # return none if a path does not exist 
        return None

    def get_goal_state_tile_locations(self):
        """ Function that helps determine where a tile is supposed to be located in the Goal State in O(1) time """
        goal_state_tile_locations = {}
        
        for y in range(len(self.goal_state)):
            for x in range(len(self.goal_state[0])):
                goal_state_tile_locations[self.goal_state[y][x]] = (y, x)

        return goal_state_tile_locations

    def compute_h(self, current_state):
        """ Heuristic Function: Sum of Manhattan Distances """
        sum_of_manhattan_distances = 0
        
        for y in range(len(current_state)):
            for x in range(len(current_state[0])):
                # skip if not a number
                if (current_state[y][x] == " "):
                    continue
                # computing sum of manhattan distances
                y_goal, x_goal = self.goal_state_tile_locations[current_state[y][x]]
                sum_of_manhattan_distances += abs(y_goal - y) + abs(x_goal - x)
        
        return sum_of_manhattan_distances
    
    def represent_current_state(self, current_state):
        print(tabulate(current_state, tablefmt="grid"))        


    def test_goal(self, current_state):
        """ Returns Whether the Current State is the Same as the Goal State """
        return current_state == self.goal_state

    def generate_successor(self, current_state_node):
        """ Assigns the Current Node as the Parent of the Next Possible Unvisited Nodes AND Returns All the Next Possible Unvisited Nodes Based on the Current State """
        # destructuring the grid and the location of the blank tile 
        current_state = current_state_node.state
        blank_tile_loc = current_state_node.blank_tile_loc

        blank_tile_y = blank_tile_loc[0]
        blank_tile_x = blank_tile_loc[1]
        
        next_state_nodes = []
        
        # Try to switch the LEFT tile with the blank tile
        if (blank_tile_x > 0):
            # get a copy of the current_state and switch the tiles
            left_shifted_grid = copy.deepcopy(current_state)
            left_shifted_grid[blank_tile_y][blank_tile_x] = left_shifted_grid[blank_tile_y][blank_tile_x - 1]
            left_shifted_grid[blank_tile_y][blank_tile_x - 1] = " "
            # add the state to the next_states
            child_node = Node(left_shifted_grid, parent = current_state_node, blank_tile_loc = (blank_tile_y, blank_tile_x - 1), g = current_state_node.g + 1, h = self.compute_h(left_shifted_grid))
            next_state_nodes.append(child_node)

        # Try to switch the TOP tile with the blank tile
        if (blank_tile_y > 0):
            # get a copy of the current_state and switch the tiles
            top_shifted_grid = copy.deepcopy(current_state)
            top_shifted_grid[blank_tile_y][blank_tile_x] = top_shifted_grid[blank_tile_y - 1][blank_tile_x]
            top_shifted_grid[blank_tile_y - 1][blank_tile_x] = " "
            # add the state to the next_states
            child_node = Node(top_shifted_grid, parent = current_state_node, blank_tile_loc = (blank_tile_y - 1, blank_tile_x), g = current_state_node.g + 1, h = self.compute_h(top_shifted_grid))
            next_state_nodes.append(child_node)


        # Try to switch the RIGHT tile with the blank tile
        if (blank_tile_x < 2):
            # get a copy of the current_state and switch the tiles
            right_shifted_grid = copy.deepcopy(current_state)
            right_shifted_grid[blank_tile_y][blank_tile_x] = right_shifted_grid[blank_tile_y][blank_tile_x + 1]
            right_shifted_grid[blank_tile_y][blank_tile_x + 1] = " "
            # add the state to the next_states
            child_node = Node(right_shifted_grid, parent = current_state_node, blank_tile_loc = (blank_tile_y, blank_tile_x + 1), g = current_state_node.g + 1, h = self.compute_h(right_shifted_grid))
            next_state_nodes.append(child_node)

        
        # Try to switch the BOTTOM tile with the blank tile
        if (blank_tile_y < 2):
            # get a copy of the current_state and switch the tiles
            bottom_shifted_grid = copy.deepcopy(current_state)
            bottom_shifted_grid[blank_tile_y][blank_tile_x] = bottom_shifted_grid[blank_tile_y + 1][blank_tile_x]
            bottom_shifted_grid[blank_tile_y + 1][blank_tile_x] = " "
            # add the state to the next_states
            child_node = Node(bottom_shifted_grid, parent = current_state_node, blank_tile_loc = (blank_tile_y + 1, blank_tile_x), g = current_state_node.g + 1, h = self.compute_h(bottom_shifted_grid))
            next_state_nodes.append(child_node)

        return next_state_nodes

    def visualize_shortest_path(self, path):
        print("Shortest path:")
        for state in reversed(path):
            self.represent_current_state(state)        
    
    def generate_successor_bfs(self, current_state, visited_list, state_parents):
        """ Returns All the Possible Next States Based on the Current State """
        # destructuring the grid and the location of the blank tile 
        current_grid, blank_tile_loc = current_state
        blank_tile_y = blank_tile_loc[0]
        blank_tile_x = blank_tile_loc[1]
        
        next_states = []
        
        # Try to switch the LEFT tile with the blank tile
        if (blank_tile_x > 0):
            # get a copy of the current_state and switch the tiles
            left_shifted_grid = copy.deepcopy(current_grid)
            left_shifted_grid[blank_tile_y][blank_tile_x] = left_shifted_grid[blank_tile_y][blank_tile_x - 1]
            left_shifted_grid[blank_tile_y][blank_tile_x - 1] = " "
            # add the state to the next_states
            if not visited_list.get(json.dumps(left_shifted_grid), False):
                next_states.append((left_shifted_grid, (blank_tile_y, blank_tile_x - 1)))
                state_parents[json.dumps(left_shifted_grid)] = json.dumps(current_grid)

        # Try to switch the TOP tile with the blank tile
        if (blank_tile_y > 0):
            # get a copy of the current_state and switch the tiles
            top_shifted_grid = copy.deepcopy(current_grid)
            top_shifted_grid[blank_tile_y][blank_tile_x] = top_shifted_grid[blank_tile_y - 1][blank_tile_x]
            top_shifted_grid[blank_tile_y - 1][blank_tile_x] = " "
            # add the state to the next_states
            if not visited_list.get(json.dumps(top_shifted_grid), False):
                next_states.append((top_shifted_grid, (blank_tile_y - 1, blank_tile_x)))
                state_parents[json.dumps(top_shifted_grid)] = json.dumps(current_grid)


        # Try to switch the RIGHT tile with the blank tile
        if (blank_tile_x < 2):
            # get a copy of the current_state and switch the tiles
            right_shifted_grid = copy.deepcopy(current_grid)
            right_shifted_grid[blank_tile_y][blank_tile_x] = right_shifted_grid[blank_tile_y][blank_tile_x + 1]
            right_shifted_grid[blank_tile_y][blank_tile_x + 1] = " "
            # add the state to the next_states
            if not visited_list.get(json.dumps(right_shifted_grid), False):
                next_states.append((right_shifted_grid, (blank_tile_y, blank_tile_x + 1)))
                state_parents[json.dumps(right_shifted_grid)] = json.dumps(current_grid)

        
        # Try to switch the BOTTOM tile with the blank tile
        if (blank_tile_y < 2):
            # get a copy of the current_state and switch the tiles
            bottom_shifted_grid = copy.deepcopy(current_grid)
            bottom_shifted_grid[blank_tile_y][blank_tile_x] = bottom_shifted_grid[blank_tile_y + 1][blank_tile_x]
            bottom_shifted_grid[blank_tile_y + 1][blank_tile_x] = " "
            # add the state to the next_states
            if not visited_list.get(json.dumps(bottom_shifted_grid), False):
                next_states.append((bottom_shifted_grid, (blank_tile_y + 1, blank_tile_x)))
                state_parents[json.dumps(bottom_shifted_grid)] = json.dumps(current_grid)


        return next_states
    

    def test_goal(self, current_state):
        """ Returns Whether the Current State is the Same as the Goal State """
        return current_state == self.goal_state

    def reconstruct_path(self, current_state_node):
        """ Returns the shortest path found """
        shortest_path = [current_state_node.state]
        
        while current_state_node.parent:
            current_state_node = current_state_node.parent
            shortest_path.append(current_state_node.state)
        
        return shortest_path

    def reconstruct_path_bfs(self, current_state, state_parents):
        """ Returns the Shortest Path from the Initial State to the Goal State """
        shortest_path = [current_state]
        while (state_parents[json.dumps(current_state)]):
            shortest_path.append(json.loads(state_parents[json.dumps(current_state)]))
            current_state = json.loads(state_parents[json.dumps(current_state)])
        return shortest_path        


# Testing the 8 Puzzle AI Agent with the A* algorithm

initial_state_1 = [
    [1, 2, 3],
    [4, " ", 6],
    [7, 5, 8]
]

initial_state_2 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, " "]
]

initial_state_3 = [
    [1, 2, 3],
    [4, 5, 6],
    [" ", 7, 8]
]

initial_state_4 = [
    [1, 2, 3],
    [5, " ", 6],
    [4, 7, 8]
]

initial_state_5 = [
    [1, 3, 6],
    [5, " ", 2],
    [4, 7, 8]
]

initial_state_6 = [
    [1, 3, 6],
    [5, " ", 7],
    [4, 8, 2]
]


goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, " "]
]

# NPuzzleAiAgent(initial_state_1, goal_state, (1, 1), "a_star")
# NPuzzleAiAgent(initial_state_2, goal_state, (2, 2), "a_star")
# NPuzzleAiAgent(initial_state_3, goal_state, (2, 0), "a_star")
# NPuzzleAiAgent(initial_state_4, goal_state, (1, 1), "a_star")
# NPuzzleAiAgent(initial_state_5, goal_state, (1, 1), "a_star")
NPuzzleAiAgent(initial_state_6, goal_state, (1, 1), "bfs")
# NPuzzleAiAgent(initial_state_6, goal_state, (1, 1), "a_star")


import matplotlib.pyplot as plt
#  The following is for the plot
# print(a_star_num_of_visited_nodes)

plt.bar(["BFS Num Of Visited Nodes", "A* Num of Visited Nodes"], [2152, 12], color='skyblue')

# Labels and title
plt.xlabel("Categories")
plt.ylabel("Values")
plt.title("Number of Nodes (States) Visited by A* vs BFS on an 8 Puzzle Where A* Has Advantage")

# Show the plot
plt.show()