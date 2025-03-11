from collections import deque
import pygame
import time
from enum import Enum
import heapq
import json
import matplotlib.pyplot as plt

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    GREY = (200, 200, 200)


class Node:
    def __init__(self, state, parent, g, h):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h
        
    def __lt__(self, other):
        """ Python's built-in sorting Method for Min-Heap Comparison """
        return self.f < other.f



class MazeAiAgent:
    def __init__(self, maze, initial_state, goal_state, algorithm):
        self.maze = maze
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.screen = None          
        self.initialize_visualization() 
        self.total_states_visited = 0
        if (algorithm == "bfs"):
            self.bfs()
        elif (algorithm == "a_star"):
            self.a_star()

    def a_star(self):
        """ Does A* on a Maze and Returns the Shortest Path from Initial State to Goal State """
        visited = set()

        min_f_heap = []
        # formulate the root state node
        root_state_h = self.compute_h(self.initial_state)
        root_state_node = Node(self.initial_state, parent = None, g = 0, h = root_state_h)
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
                self.draw_shortest_path(self.reconstruct_path_a_star(current_state_node))
                self.total_states_visited = len(visited)
                print(len(visited))
                return
            
            # mark the current state as visited
            current_state = current_state_node.state
            if (current_state not in visited):
                visited.add(current_state)
                # assign and retrieve successor nodes
                next_state_nodes = self.generate_successor_a_star(current_state_node)
                for state_node in next_state_nodes:
                    heapq.heappush(min_f_heap, state_node)
            
            self.mark_as_visited(current_state)
        
        # return none if a path does not exist 
        return None

    def generate_successor_a_star(self, current_state_node):
        """ Returns the possible next states from the current state """
        current_y = current_state_node.state[0]
        current_x = current_state_node.state[1]
        next_state_nodes = []

        # check if LEFT block is within the maze
        if (current_x > 0):
            # add the path if it is not a wall 
            if (self.maze[current_y][current_x - 1] == " "):
                # add the state to the next_states
                child_node = Node((current_y, current_x - 1), parent = current_state_node, g = current_state_node.g + 1, h = self.compute_h((current_y, current_x - 1)))
                next_state_nodes.append(child_node)

        # check if TOP block is within the maze
        if (current_y > 0):
            if (self.maze[current_y - 1][current_x] == " "):
                child_node = Node((current_y - 1, current_x), parent = current_state_node, g = current_state_node.g + 1, h = self.compute_h((current_y - 1, current_x)))
                next_state_nodes.append(child_node)

        # check if RIGHT block is within the maze
        if (current_x < len(self.maze[0]) - 1):
            if (self.maze[current_y][current_x + 1] == " "):
                child_node = Node((current_y, current_x + 1), parent = current_state_node, g = current_state_node.g + 1, h = self.compute_h((current_y, current_x + 1)))
                next_state_nodes.append(child_node)

        # check if BOTTOM block is within the maze
        if (current_y < len(self.maze) - 1):
            if (self.maze[current_y + 1][current_x] == " "):
                child_node = Node((current_y + 1, current_x), parent = current_state_node, g = current_state_node.g + 1, h = self.compute_h((current_y + 1, current_x)))
                next_state_nodes.append(child_node)

        return next_state_nodes


    def reconstruct_path_a_star(self, current_state_node):
        """ Returns the shortest path found """
        shortest_path = [current_state_node.state]
        
        while current_state_node.parent:
            current_state_node = current_state_node.parent
            shortest_path.append(current_state_node.state)
        
        return shortest_path
    
    def compute_h(self, current_state):
        """ Heuristic Function: Sum of Manhattan Distances """
        y_goal, x_goal = self.goal_state
        y, x = current_state
        
        return abs(y_goal - y) + abs(x_goal - x)


    def bfs(self):
        """ Does BFS on a Maze and Returns the Shortest Path from Initial State to Goal State """
        # visited
        visited = set()
        # initialize the queue
        queue = deque()
        queue.append(self.initial_state)

        # storage for parent states
        state_parents = {self.initial_state: None}

        # start the search
        while queue:
            current_state = queue.popleft()

            # check if current state has already been visited
            if (self.maze[current_state[0]][current_state[1]] == "V"):
                continue

            # represent the current state on the screen
            self.represent_current_state(current_state)

            # check if the current state is the same as the goal state
            goal_state_reached = self.test_goal(current_state)
            
            if (goal_state_reached):
                print("Goal reached")
                # reconstruct the shortest path from initial state to goal state
                path = self.reconstruct_path(state_parents, current_state)
                # draw that path visually on the screen
                self.draw_shortest_path(path)
                self.total_states_visited = len(visited)
                return

            # get the possible successor states 
            possible_next_states = self.generate_successor(current_state)

            # append all the next states in the queue
            # update the parent of each state
            for state in possible_next_states:
                queue.append(state)
                state_parents[state] = current_state
            
            # mark the current state (block) as visited
            visited.add(current_state)
            self.mark_as_visited(current_state)

        print("No path found")
        return None        

    def represent_current_state(self, current_state):
        """ Draws a BLUE rect on the current state (x, y locations) """
        pygame.draw.rect(self.screen, Color.BLUE.value, (current_state[1] * 30, current_state[0] * 30, 30, 30))
        pygame.draw.rect(self.screen, Color.GREY.value, (current_state[1] * 30, current_state[0] * 30, 30, 30), 1)
        pygame.display.update()
        # pause for a bit to make it easier to follow up with the ai agent
        time.sleep(0.10)


    def generate_successor(self, current_state):
        """ Returns the possible next states from the current state """
        current_y = current_state[0]
        current_x = current_state[1]
        possible_next_states = []

        # check if LEFT block is within the maze
        if (current_x > 0):
            # add the path if it is not a wall 
            if (self.maze[current_y][current_x - 1] == " "):
                possible_next_states.append((current_y, current_x - 1))
        
        # check if TOP block is within the maze
        if (current_y > 0):
            if (self.maze[current_y - 1][current_x] == " "):
                possible_next_states.append((current_y - 1, current_x))

        # check if RIGHT block is within the maze
        if (current_x < len(self.maze[0]) - 1):
            if (self.maze[current_y][current_x + 1] == " "):
                possible_next_states.append((current_y, current_x + 1))

        # check if BOTTOM block is within the maze
        if (current_y < len(self.maze) - 1):
            if (self.maze[current_y + 1][current_x] == " "):
                possible_next_states.append((current_y + 1, current_x))
                        
        return possible_next_states


    def test_goal(self, current_state):
        """ Returns TRUE if the current state and the goal state are the same, otherwise FALSE """
        return current_state == self.goal_state
        
    def reconstruct_path(self, parent, current_state):
        """ Backtracks the goal state's parent states to determine the shortest path from the initial state to goal state """
        shortest_path = [current_state]
        while (parent[current_state]):
            shortest_path.append(parent[current_state])
            current_state = parent[current_state]
        return shortest_path


    def mark_as_visited(self, current_state):
        """ Updates the current state as Visited and sets the Color of the Current State to Orange Instead of Blue """
        self.maze[current_state[0]][current_state[1]] = "V"
        pygame.draw.rect(self.screen, Color.YELLOW.value, (current_state[1] * 30, current_state[0] * 30, 30, 30))
        pygame.draw.rect(self.screen, Color.GREY.value, (current_state[1] * 30, current_state[0] * 30, 30, 30), 1)
        pygame.display.update()
        # pause for a bit to make it easier to follow up with the ai agent
        time.sleep(0.10)

    
    def draw_shortest_path(self, shortest_path):
        """ Draws the Shortest Path to reach the Goal State from the Initial State """
        for route in shortest_path:
            pygame.draw.rect(self.screen, Color.GREEN.value, (route[1] * 30, route[0] * 30, 30, 30))
            pygame.draw.rect(self.screen, Color.GREY.value, (route[1] * 30, route[0] * 30, 30, 30), 1)
            pygame.display.update()
            # pause for a bit to make it easier to follow up with the ai agent
            time.sleep(4.00)

            


    def initialize_visualization(self):
        """ Draws the Maze with the Initial State and the Goal State """
        width = len(self.maze[0])
        height = len(self.maze)

        # Initialize pygame and set the screen size
        pygame.init()
        self.screen = pygame.display.set_mode((width * 30, height * 30))
        pygame.display.set_caption("Uninformed (BFS) AI Agent Solving the Maze Problem")

        # Draw the initial grid on the screen
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                # default color of a block
                current_cell_color = Color.BLACK.value
                if (y == self.goal_state[0] and x == self.goal_state[1]):
                    current_cell_color = Color.GREEN.value
                elif (y == self.initial_state[0] and x == self.initial_state[1]):
                    current_cell_color = Color.RED.value    
                elif (self.maze[y][x] == " "):
                    current_cell_color = Color.WHITE.value
                
                # draw the current block
                pygame.draw.rect(self.screen, current_cell_color, (x * 30, y * 30, 30, 30))
                # draw a grey border around it
                pygame.draw.rect(self.screen, Color.GREY.value, (x * 30, y * 30, 30, 30), 1)
        
        # apply the changes
        pygame.display.update()
        # pause for a bit to make it easier to follow up with the ai agent
        time.sleep(1.00)


maze_a_star_no_advantage = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "#", " ", "#", "#", " ", "#", " ", " ", "#"],
    ["#", "#", " ", " ", "#", "#", " ", " ", "#", "#"],
    ["#", " ", "#", " ", "#", "#", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", "#"],
    ["#", " ", " ", " ", "#", "#", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", " ", " ", "#", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

maze_a_star_has_advantage = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", "#", " ", " ", "#", "#"],
    ["#", " ", "#", " ", "#", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

# Please uncomment either one of the following search algorithms and run

#  BFS
bfs_num_of_visited_nodes = MazeAiAgent(maze = maze_a_star_has_advantage, initial_state = (8, 1), goal_state = (1, 2), algorithm = "a_star").total_states_visited

# A*
# a_star_num_of_visited_nodes = MazeAiAgent(maze = maze_a_star_no_advantage, initial_state = (8, 1), goal_state = (1, 2), algorithm = "a_star").total_states_visited
 
#  The following is for the plot
# print(a_star_num_of_visited_nodes)

# plt.bar(["BFS Num Of Visited Nodes", "A* Num of Visited Nodes"], [27, 9], color='skyblue')

# # Labels and title
# plt.xlabel("Categories")
# plt.ylabel("Values")
# plt.title("Number of Nodes (States) Visited by A* vs BFS on a Maze Where A* Has Advantage")

# # Show the plot
# plt.show()