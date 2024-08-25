import unittest
import numpy as np
from TEST.shared_memory_test.shared_memory_manager import SharedMemoryManager

class TestSharedMemoryManager(unittest.TestCase):
    def setUp(self):
        self.max_agents = 10
        self.dimensions = 2
        self.smm = SharedMemoryManager(self.max_agents, self.dimensions)

    def test_add_agent(self):
        position = [1.0, 2.0]
        index = self.smm.add_agent(position)
        self.assertEqual(index, 0)
        self.assertEqual(self.smm.current_agent_count.value, 1)
        np.testing.assert_array_equal(self.smm.get_positions(), [position])

    def test_remove_agent(self):
        position = [1.0, 2.0]
        index = self.smm.add_agent(position)
        self.assertTrue(self.smm.remove_agent(index))
        self.assertEqual(self.smm.current_agent_count.value, 0)
        self.assertEqual(len(self.smm.get_positions()), 0)

    def test_update_positions(self):
        self.smm.add_agent([1.0, 2.0])
        self.smm.add_agent([3.0, 4.0])
        new_positions = np.array([[5.0, 6.0], [7.0, 8.0]])
        self.smm.update_positions(new_positions)
        np.testing.assert_array_equal(self.smm.get_positions(), new_positions)

    def test_max_agents(self):
        for i in range(self.max_agents):
            self.assertNotEqual(self.smm.add_agent([float(i), float(i)]), -1)
        self.assertEqual(self.smm.add_agent([100.0, 100.0]), -1)

if __name__ == '__main__':
    unittest.main()