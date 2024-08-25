import multiprocessing as mp
import numpy as np
import random
import time

class SharedMemoryManager:
    def __init__(self, max_agents, dimensions):
        self.max_agents = max_agents
        self.dimensions = dimensions
        self.positions = mp.Array('f', max_agents * dimensions)
        self.agent_ids = mp.Array('i', max_agents)
        self.active_mask = mp.Array('i', max_agents)
        self.current_agent_count = mp.Value('i', 0)
        self.next_agent_id = mp.Value('i', 0)
        self.agent_changes = mp.Queue()
        self.lock = mp.Lock()

    def add_agent(self, position):
        with self.lock:
            if self.current_agent_count.value < self.max_agents:
                index = self.current_agent_count.value
                np_positions = np.frombuffer(self.positions.get_obj(), dtype=np.float32).reshape(self.max_agents, self.dimensions)
                np_positions[index] = position
                self.agent_ids[index] = self.next_agent_id.value
                self.active_mask[index] = 1
                self.current_agent_count.value += 1
                self.next_agent_id.value += 1
                self.agent_changes.put(('add', self.agent_ids[index]))
                return self.agent_ids[index]
            return -1

    def remove_agent(self, agent_id):
        with self.lock:
            np_agent_ids = np.frombuffer(self.agent_ids.get_obj(), dtype=np.int32)
            index = np.where(np_agent_ids == agent_id)[0]
            if len(index) > 0:
                index = index[0]
                self.active_mask[index] = 0
                self.current_agent_count.value -= 1
                self.agent_changes.put(('remove', agent_id))
                return True
            return False

    def get_data_for_tensorflow(self):
        with self.lock:
            np_positions = np.frombuffer(self.positions.get_obj(), dtype=np.float32).reshape(self.max_agents, self.dimensions)
            np_active_mask = np.frombuffer(self.active_mask.get_obj(), dtype=np.int32)
            active_indices = np.where(np_active_mask == 1)[0]
            return np_positions[active_indices]

    def get_data_for_box2d(self):
        with self.lock:
            np_positions = np.frombuffer(self.positions.get_obj(), dtype=np.float32).reshape(self.max_agents, self.dimensions)
            np_agent_ids = np.frombuffer(self.agent_ids.get_obj(), dtype=np.int32)
            np_active_mask = np.frombuffer(self.active_mask.get_obj(), dtype=np.int32)
            active_indices = np.where(np_active_mask == 1)[0]
            return list(zip(np_agent_ids[active_indices], np_positions[active_indices]))

    def get_data_for_visual(self):
        return self.get_data_for_tensorflow()

    def update_positions(self, new_positions):
        with self.lock:
            np_positions = np.frombuffer(self.positions.get_obj(), dtype=np.float32).reshape(self.max_agents, self.dimensions)
            np_active_mask = np.frombuffer(self.active_mask.get_obj(), dtype=np.int32)
            active_indices = np.where(np_active_mask == 1)[0]
            if len(active_indices) == len(new_positions):
                np_positions[active_indices] = new_positions
            else:
                print(f"Warning: Mismatch in number of active agents ({len(active_indices)}) and new positions ({len(new_positions)})")


class Ecosystem:
    def __init__(self, shared_memory):
        self.shared_memory = shared_memory

    def step(self):
        # Simulate ecosystem logic
        positions = self.shared_memory.get_data_for_tensorflow()
        if len(positions) > 0:
            new_positions = positions + np.random.uniform(-0.1, 0.1, positions.shape)
            self.shared_memory.update_positions(new_positions)

        # Randomly add or remove agents
        if random.random() < 0.1:  # 10% chance to add an agent
            self.add_agent()
        if random.random() < 0.05:  # 5% chance to remove an agent
            self.remove_agent()

    def add_agent(self):
        position = np.random.rand(2)  # 2D position
        agent_id = self.shared_memory.add_agent(position)
        if agent_id != -1:
            print(f"Added agent {agent_id}")

    def remove_agent(self):
        data = self.shared_memory.get_data_for_box2d()
        if data:
            agent_id = random.choice(data)[0]
            if self.shared_memory.remove_agent(agent_id):
                print(f"Removed agent {agent_id}")

class Box2DSimulation:
    def __init__(self, shared_memory):
        self.shared_memory = shared_memory

    def step(self):
        # Simulate Box2D physics (simplified)
        data = self.shared_memory.get_data_for_box2d()
        if data:
            new_positions = [pos + np.random.uniform(-0.05, 0.05, 2) for _, pos in data]
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

def ecosystem_loop(shared_memory, running):
    ecosystem = Ecosystem(shared_memory)
    while running.value:
        ecosystem.step()
        time.sleep(0.01)

def box2d_loop(shared_memory, running):
    box2d_sim = Box2DSimulation(shared_memory)
    while running.value:
        box2d_sim.step()
        time.sleep(0.01)

def tf_loop(shared_memory, running):
    tf_sim = TensorFlowSimulation(shared_memory)
    while running.value:
        forces = tf_sim.calculate_forces()
        if len(forces) > 0:
            shared_memory.update_positions(forces)  # Simplified: using forces as position updates
        time.sleep(0.01)

def visual_system_loop(shared_memory, running):
    visual_system = VisualSystem(shared_memory)
    while running.value:
        visual_system.draw()
        time.sleep(0.1)

def run_simulation():
    max_agents = 1000
    dimensions = 2
    shared_memory = SharedMemoryManager(max_agents, dimensions)
    running = mp.Value('i', 1)

    processes = [
        mp.Process(target=ecosystem_loop, args=(shared_memory, running)),
        mp.Process(target=box2d_loop, args=(shared_memory, running)),
        mp.Process(target=tf_loop, args=(shared_memory, running)),
        mp.Process(target=visual_system_loop, args=(shared_memory, running))
    ]

    for process in processes:
        process.start()

    try:
        time.sleep(30)  # Run simulation for 30 seconds
    finally:
        running.value = 0
        for process in processes:
            process.join()

if __name__ == "__main__":
    run_simulation()
