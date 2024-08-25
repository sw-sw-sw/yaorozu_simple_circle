import multiprocessing as mp
import time
import numpy as np 
from subsystems import TensorFlowSimulation , Box2DSimulation, Ecosystem, VisualSystem, SharedMemoryManager

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
            shared_memory.update_forces(forces)
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

    # Add some initial agents
    for _ in range(10):
        shared_memory.add_agent(np.random.rand(dimensions))

    try:
        time.sleep(10)  # Run simulation for 10 seconds
    finally:
        running.value = 0
        for process in processes:
            process.join()

if __name__ == "__main__":
    run_simulation()
