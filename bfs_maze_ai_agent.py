from collections import deque
import pygame
import time
from enum import Enum

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    GREY = (200, 200, 200)


class BfsMazeAiAgent:
    def __init__(self, maze, initial_state, goal_state):
        self.maze = maze
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.screen = None          
        self.initialize_visualization() 
        self.bfs()


    def bfs(self):
        """ Does BFS on a Maze and Returns the Shortest Path from Initial State to Goal State """
        # initialize the queue
        queue = deque()
        queue.append(self.initial_state)

        # storage for parent states
        state_parents = {self.initial_state: None}

        # start the search
        while queue:
            current_state = queue.popleft()

            # check if current state has already been visited
            if (maze[current_state[0]][current_state[1]] == "V"):
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
                return path

            # get the possible successor states 
            possible_next_states = self.generate_successor(current_state)

            # append all the next states in the queue
            # update the parent of each state
            for state in possible_next_states:
                queue.append(state)
                state_parents[state] = current_state
            
            # mark the current state (block) as visited
            self.mark_as_visited(current_state)

        print("No path found")
        return None        

    def represent_current_state(self, current_state):
        """ Draws a BLUE rect on the current state (x, y locations) """
        pygame.draw.rect(self.screen, Color.BLUE.value, (current_state[1] * 30, current_state[0] * 30, 30, 30))
        pygame.draw.rect(self.screen, Color.GREY.value, (current_state[1] * 30, current_state[0] * 30, 30, 30), 1)
        pygame.display.update()
        # pause for a bit to make it easier to follow up with the ai agent
        time.sleep(0.40)


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
        time.sleep(0.40)

    
    def draw_shortest_path(self, shortest_path):
        """ Draws the Shortest Path to reach the Goal State from the Initial State """
        for route in shortest_path:
            pygame.draw.rect(self.screen, Color.GREEN.value, (route[1] * 30, route[0] * 30, 30, 30))
            pygame.draw.rect(self.screen, Color.GREY.value, (route[1] * 30, route[0] * 30, 30, 30), 1)
            pygame.display.update()
            # pause for a bit to make it easier to follow up with the ai agent
            time.sleep(1.00)

            


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


maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    [" ", " ", " ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", "#", " ", "#", " ", "#", " ", " ", "#", "#"],
    ["#", " ", " ", "#", " ", "#", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", "#", " ", "#", " ", "#", "#"],
    ["#", " ", "#", "#", "#", "#", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

BfsMazeAiAgent(maze = maze, initial_state = (5, 8), goal_state = (4, 5))