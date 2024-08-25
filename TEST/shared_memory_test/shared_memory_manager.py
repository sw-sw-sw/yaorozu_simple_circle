import multiprocessing as mp
import numpy as np

class SharedMemoryManager:
    def __init__(self, max_agents, dimensions):
        self.max_agents = max_agents
        self.dimensions = dimensions
        self.positions = mp.Array('f', max_agents * dimensions)
        self.active_mask = mp.Array('i', max_agents)
        self.current_agent_count = mp.Value('i', 0)
        self.lock = mp.Lock()

    def add_agent(self, position):
        with self.lock:
            if self.current_agent_count.value < self.max_agents:
                index = self.current_agent_count.value
                np_positions = np.frombuffer(self.positions.get_obj(), dtype=np.float32).reshape(self.max_agents, self.dimensions)
                np_positions[index] = position
                self.active_mask[index] = 1
                self.current_agent_count.value += 1
                return index
            return -1

    def remove_agent(self, index):
        with self.lock:
            if 0 <= index < self.max_agents and self.active_mask[index] == 1:
                self.active_mask[index] = 0
                self.current_agent_count.value -= 1
                return True
            return False

    def get_positions(self):
        with self.lock:
            np_positions = np.frombuffer(self.positions.get_obj(), dtype=np.float32).reshape(self.max_agents, self.dimensions)
            np_active_mask = np.frombuffer(self.active_mask.get_obj(), dtype=np.int32)
            return np_positions[np_active_mask == 1]

    def update_positions(self, new_positions):
        with self.lock:
            np_positions = np.frombuffer(self.positions.get_obj(), dtype=np.float32).reshape(self.max_agents, self.dimensions)
            np_active_mask = np.frombuffer(self.active_mask.get_obj(), dtype=np.int32)
            np_positions[np_active_mask == 1] = new_positions