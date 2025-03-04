from collections import deque
import pygame
import time
from tabulate import tabulate
import json
import copy

class BfsEightPuzzleAiAgent:
    def __init__(self, initial_state, goal_state, initial_blank_tile_loc):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.blank_tile_location = initial_blank_tile_loc
        self.bfs()
        # self.initialize_visualization()
    
    def bfs(self):
        """ """
        # initialize the queue
        queue = deque()
        queue.append((initial_state, self.blank_tile_location))

        visited_list = {}

        while queue:
            current_state, blank_tile_location = queue.popleft()

            # skip if visited; o.w. mark as visited 
            # if (json.dumps(current_state) in visited_list):
            #     continue
            # else:
            #     visited_list[json.dumps(current_state)] = True

            self.represent_current_state(current_state)

            goal_reached = self.test_goal(current_state)

            if (goal_reached):
                print("Goal reached!")
                break

            next_states = self.generate_successor((current_state, blank_tile_location), visited_list)

            for state in next_states:
                queue.append(state)

            visited_list[json.dumps(current_state)] = True
            


    def represent_current_state(self, current_state):
        print(tabulate(current_state, tablefmt="grid"))        

    def generate_successor(self, current_state, visited_list):
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

        # Try to switch the TOP tile with the blank tile
        if (blank_tile_y > 0):
            # get a copy of the current_state and switch the tiles
            top_shifted_grid = copy.deepcopy(current_grid)
            top_shifted_grid[blank_tile_y][blank_tile_x] = top_shifted_grid[blank_tile_y - 1][blank_tile_x]
            top_shifted_grid[blank_tile_y - 1][blank_tile_x] = " "
            # add the state to the next_states
            if not visited_list.get(json.dumps(top_shifted_grid), False):
                next_states.append((top_shifted_grid, (blank_tile_y - 1, blank_tile_x)))

        # Try to switch the RIGHT tile with the blank tile
        if (blank_tile_x < 2):
            # get a copy of the current_state and switch the tiles
            right_shifted_grid = copy.deepcopy(current_grid)
            right_shifted_grid[blank_tile_y][blank_tile_x] = right_shifted_grid[blank_tile_y][blank_tile_x + 1]
            right_shifted_grid[blank_tile_y][blank_tile_x + 1] = " "
            # add the state to the next_states
            if not visited_list.get(json.dumps(right_shifted_grid), False):
                next_states.append((right_shifted_grid, (blank_tile_y, blank_tile_x + 1)))
        
        # Try to switch the BOTTOM tile with the blank tile
        if (blank_tile_y < 2):
            # get a copy of the current_state and switch the tiles
            bottom_shifted_grid = copy.deepcopy(current_grid)
            bottom_shifted_grid[blank_tile_y][blank_tile_x] = bottom_shifted_grid[blank_tile_y + 1][blank_tile_x]
            bottom_shifted_grid[blank_tile_y + 1][blank_tile_x] = " "
            # add the state to the next_states
            if not visited_list.get(json.dumps(bottom_shifted_grid), False):
                next_states.append((bottom_shifted_grid, (blank_tile_y + 1, blank_tile_x)))

        return next_states
    

    def test_goal(self, current_state):
        """ Returns Whether the Current State is the Same as the Goal State """
        return current_state == self.goal_state


    def reconstruct_path(self):
        print()

    def initialize_visualization(self):
        """ Draws the Maze with the Initial State and the Goal State """
        width = 3
        height = 3
        
        # Initialize pygame and set the screen size
        pygame.init()
        self.screen = pygame.display.set_mode((width * 60, height * 60))
        pygame.display.set_caption("Uninformed (BFS) AI Agent Solving the 8 Puzzle Problem")
        # setting default font size as 36
        font = pygame.font.Font(None, 36)

        # Draw the initial grid on the screen
        for y in range(3):
            for x in range(3):
                # draw the background tile
                pygame.draw.rect(self.screen, (255, 255, 255), (x * 60, y * 60, 60, 60))
                # get the number 
                number = str(self.initial_state[y][x])
                # prepare the black text rendering
                text_surface = font.render(number, True, (0, 0, 0))
                # center it in the corresponding cell
                text_rect = text_surface.get_rect(center=(x * 60 + 30, y * 60 + 30))
                # apply the placements
                self.screen.blit(text_surface, text_rect)
                # draw a grey border around the cell
                pygame.draw.rect(self.screen, (200, 200, 200), (x * 60, y * 60, 60, 60), 1)
        # apply all the changes
        pygame.display.update()
        # pause for a bit to make it easier to follow up with the ai agent
        time.sleep(5.00)






initial_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, " ", 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, " "]
]

BfsEightPuzzleAiAgent(initial_state, goal_state, (2, 1))