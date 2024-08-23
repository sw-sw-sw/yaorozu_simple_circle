# box2d_simulation.py
from Box2D import b2World, b2Vec2, b2BodyDef, b2_dynamicBody, b2CircleShape
from config import *
import numpy as np

class Box2DSimulation:
    def __init__(self, world_width, world_height):
        self.world = b2World(gravity=(0, 0), doSleep=True)
        self.bodies = []

    def create_bodies(self, initial_positions, initial_velocities):
        for position, velocity in zip(initial_positions, initial_velocities):
            body_def = b2BodyDef(
                type=b2_dynamicBody,
                position=b2Vec2(float(position[0]), float(position[1])),  # ここを修正
                linearVelocity=b2Vec2(float(velocity[0]), float(velocity[1])),  # 速度を設定
                linearDamping=LINEAR_DAMPING
            )
            body = self.world.CreateBody(body_def)
            circle_shape = b2CircleShape(radius=AGENT_RADIUS)
            body.CreateFixture(shape=circle_shape, 
                               density=AGENT_DENSITY, 
                               friction=AGENT_FRICTION,
                               restitution=AGENT_RESTITUTION
                               )
            rnd = np.random.rand() * 1.4 + 1.5
            body.mass = AGENT_MASS * rnd
            self.bodies.append(body)

    def apply_forces(self, forces):
        for body, force in zip(self.bodies, forces):
            body.ApplyForceToCenter((float(force[0]), float(force[1])), wake=True)  # ここも修正

    def step(self):
        self.world.Step(DT, 6, 2)

    def get_positions(self):
        return [(body.position.x, body.position.y) for body in self.bodies]  # この行を修正

