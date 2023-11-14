import gym 
from gymnasium import spaces 
import numpy as np 
import pygame
from shapely.geometry import Polygon
import time as time 
import random

class SpaDesWorldEnv(gym.Env):
    def __init__(self, site=Polygon([(500, 216.50635094610966),(850.0, 500.0),(500.0, 783.4936490538903),(150.0, 783.4936490538903),(500.0, 500.0),(500.0, 216.50635094610966)]), size=850): 
        """
        The environment for generating building polygons for a given site boundary for SUTD Spatial Design Studio 2023.

        Args: 
            sites (list): list of sites to be generated 
            size (tuple): size of the grid in pixels, in the form (width, height)
        """
        self.site = site
        self.size = size  # The size of the square grid
        self.buildings = [[100,100,100,100]] # list of buildings
        # self.num_agents 

        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Dict({"site_area": spaces.Box(0, size - 1, shape=(size, size, 3), dtype=np.float32), "buildings": spaces.Box(0,size-1, shape=(1,4))})
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
            4: np.array([0, 0]),
        }
        self.step_size=20

    def __get_obs__(self): 
        return {"site_area": self._render_frame(), "buildings":self.buildings}, {}

    def __get_info__(self): 
        pass 

    def reset(self, seed=None, options=None): 
        super().reset(seed=seed)
        #spawn random building 
        size = random.randint(50,100)
        self.buildings = []
        self.buildings.append([random.randint(100, self.size-100),random.randint(100, self.size-100),size,size])
        observation, info = self.__get_obs__()
        return observation, info
      
    def step(self, action): 
        action = self._action_to_direction[action]
        building = self.buildings[0]
        building = np.concatenate([np.clip(building[:2] + action*self.step_size, 0, self.size-1), [building[2], building[3]]])
        self.buildings[0] = building
        
        reward = 0 
        terminated = False
        for building in self.buildings: 
            if self.site.contains(Polygon([(building[0],building[1]),(building[0]+building[2],building[1]),(building[0]+building[2],building[1]+building[3]),(building[0],building[1]+building[3])])): 
                reward = 20
                terminated = True
            else: 
                dist = self.site.distance(Polygon([(building[0],building[1]),(building[0]+building[2],building[1]),(building[0]+building[2],building[1]+building[3]),(building[0],building[1]+building[3])]))
                reward = int(dist/20) * (-1) - 1
        observation, info = self.__get_obs__()
        # self.render()

        return observation, reward, terminated, False, info

    def render(self): 
        return self._render_frame() 
    
    def _render_frame(self):
        self.window_size = 850
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        self.clock = pygame.time.Clock()
        self.window.fill((255, 255, 255))
        scaled_vertices = [[int(x), int(y)] for x, y in self.site.exterior.coords]
        pygame.draw.polygon(self.window, (0, 0, 255), scaled_vertices)
        for building in self.buildings: 
            building_polygon = Polygon([(building[0],building[1]),(building[0]+building[2],building[1]),(building[0]+building[2],building[1]+building[3]),(building[0],building[1]+building[3])])
            pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(building[0],building[1],building[2],building[3]))
        # pygame.display.flip()
        pygame.display.update()
        screen_surface = pygame.display.get_surface()
        pixel_array = pygame.surfarray.array3d(screen_surface)
        self.window.blit(self.window, self.window.get_rect())
        return pixel_array



if __name__ == "__main__": 
    env = SpaDesWorldEnv()
    env.reset()
    env.render()
    env.step(2)
    env.render()
    env.reset()
    env.render()