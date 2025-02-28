import unittest

from taogod_terminal.adapters.github.static_adapter import StaticGithubAdapter
from taogod_terminal.adapters.github.base_adapter import BaseGithubAdapter

NONEMPTY_SUBNET_ROADMAPS = [
    19,
    4,
    9,
    1,
    29,
    13,
    51,
    24,
    52,
    25,
    11,
    31,
    30,
    21,
    20,
    37,
    23,
    2,
    43,
    32,
    41,
    40,
]

class TestBaseGithubAdapter(unittest.TestCase):
    def test_cannot_instantiate_abstract_class(self):
        with self.assertRaises(TypeError):
            BaseGithubAdapter()

    def test_subclasses_must_implement_get_subnet_roadmap(self):
        class IncompleteGithubAdapter(BaseGithubAdapter):
            pass

        with self.assertRaises(TypeError):
            IncompleteGithubAdapter()

    def test_concrete_implementation(self):
        class ConcreteGithubAdapter(BaseGithubAdapter):
            def get_subnet_roadmap(self, subnet_id: int) -> str:
                return f"Roadmap for subnet {subnet_id}"

        adapter = ConcreteGithubAdapter()
        for sn_id in NONEMPTY_SUBNET_ROADMAPS:
            self.assertGreater(len(adapter.get_subnet_roadmap(sn_id)), 0)

class TestStaticGithubAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = StaticGithubAdapter()

    def test_existing_subnets(self):
        for sn_id in NONEMPTY_SUBNET_ROADMAPS:
            self.assertGreater(len(self.adapter.get_subnet_roadmap(sn_id)), 0)

    def test_non_existent_subnets(self):
        roadmap = self.adapter.get_subnet_roadmap(9999)
        self.assertEqual(roadmap, "")

if __name__ == "__main__":
    unittest.main()
