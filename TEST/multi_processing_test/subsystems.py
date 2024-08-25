import numpy as np
import time
import multiprocessing as mp

class Ecosystem:
    def __init__(self, shared_memory):
        self.shared_memory = shared_memory

    def step(self):
        # Simulate ecosystem logic
        positions = self.shared_memory.get_data_for_tensorflow()
        if len(positions) > 0:
            new_positions = positions + np.random.uniform(-0.1, 0.1, positions.shape)
            self.shared_memory.update_positions(new_positions)

class Box2DSimulation:
    def __init__(self, shared_memory):
        self.shared_memory = shared_memory

    def step(self):
        # Simulate Box2D physics
        positions = self.shared_memory.get_data_for_box2d()
        if len(positions) > 0:
            new_positions = positions + np.random.uniform(-0.05, 0.05, positions.shape)
            self.shared_memory.update_positions(new_positions)

class TensorFlowSimulation:
    def __init__(self, shared_memory):
        self.shared_memory = shared_memory

    def calculate_forces(self):
        # Simulate force calculation
        positions = self.shared_memory.get_data_for_tensorflow()
        if len(positions) > 0:
            return np.random.uniform(-1, 1, positions.shape)
        return np.array([])

class VisualSystem:
    def __init__(self, shared_memory):
        self.shared_memory = shared_memory

    def draw(self):
        positions = self.shared_memory.get_data_for_visual()
        print(f"Drawing {len(positions)} agents")

class SharedMemoryManager:
    def __init__(self, max_agents, dimensions):
        self.max_agents = max_agents
        self.dimensions = dimensions
        self.positions = mp.Array('f', max_agents * dimensions)
        self.active_mask = mp.Array('i', max_agents)
        self.current_agent_count = mp.Value('i', 0)
        self.initialization_complete = mp.Value('i', 0)
        self.agent_changes = mp.Queue()
        self.lock = mp.Lock()

    def add_agent(self, position):
        with self.lock:
            if self.current_agent_count.value < self.max_agents:
                index = self.current_agent_count.value
                np_positions = np.frombuffer(self.positions.get_obj(), dtype=np.float32).reshape(self.max_agents, self.dimensions)
                np_positions[index] = position
                self.active_mask[index] = 1
                self.current_agent_count.value += 1
                self.agent_changes.put(('add', index))
                return index
            return -1

    def remove_agent(self, index):
        with self.lock:
            if 0 <= index < self.max_agents and self.active_mask[index] == 1:
                self.active_mask[index] = 0
                self.current_agent_count.value -= 1
                self.agent_changes.put(('remove', index))
                return True
            return False

    def get_data_for_tensorflow(self):
        with self.lock:
            np_positions = np.frombuffer(self.positions.get_obj(), dtype=np.float32).reshape(self.max_agents, self.dimensions)
            np_active_mask = np.frombuffer(self.active_mask.get_obj(), dtype=np.int32)
            return np_positions[np_active_mask == 1]

    def get_data_for_box2d(self):
        return self.get_data_for_tensorflow()

    def get_data_for_visual(self):
        return self.get_data_for_tensorflow()

    def update_positions(self, new_positions):
        with self.lock:
            np_positions = np.frombuffer(self.positions.get_obj(), dtype=np.float32).reshape(self.max_agents, self.dimensions)
            np_active_mask = np.frombuffer(self.active_mask.get_obj(), dtype=np.int32)
            np_positions[np_active_mask == 1] = new_positions
