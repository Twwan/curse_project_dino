import unittest
from main import create_cactus_arr, check_collision, find_radius


cactus_arr = []


class TestClass(unittest.TestCase):
    def test_collision(self):
        self.assertEqual(check_collision(create_cactus_arr(cactus_arr)), False)

        self.assertEqual(check_collision(create_cactus_arr([])), False)

    def test_radius(self):
        self.assertIsNotNone(find_radius(create_cactus_arr(cactus_arr)))

        self.assertIsNotNone(find_radius(create_cactus_arr([])))
