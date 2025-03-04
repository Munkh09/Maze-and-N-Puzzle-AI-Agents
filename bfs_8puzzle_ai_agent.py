from collections import deque
import pygame
import time

class BfsEightPuzzleAiAgent:
    def __init__(self, initial_state, goal_state, initial_blank_tile_loc):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.blank_tile_location = initial_blank_tile_loc
        self.initialize_visualization()
    
    def bfs(self):
        queue = deque()
        queue.append((initial_state, blank_tile_location))

        while queue:
            current_state = queue.popleft()

            self.represent_current_state(current_state)

            goal_reached = self.test_goal(current_state)

            if (goal_reached):
                print("Goal Reached!")

            self.generate_successor(current_state)

    def represent_current_state(self, current_state):
        print()        

    def generate_successor(self, current_state):
        # destructuring the grid and the location of the blank tile 
        current_grid, blank_tile_loc = current_state
        blank_tile_y = blank_tile_loc[0]
        blank_tile_x = blank_tile_loc[1]
        
        next_states = []
        # Try to switch the LEFT tile with the blank tile
        if (blank_tile_x > 0):
            # get a copy of the current_state and switch the tiles
            left_shifted_grid = current_grid.copy()
            left_shifted_grid[blank_tile_y][blank_tile_x] = left_shifted_grid[blank_tile_y][blank_tile_x - 1]
            left_shifted_grid[blank_tile_y][blank_tile_x - 1] = " "

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
    [8, 2, " "],
    [3, 4, 7],
    [5, 1, 6]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, " "]
]

BfsEightPuzzleAiAgent(initial_state, goal_state, (0, 2))