"""
Tests for the vacuum robot environment.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import vacuum_env

def test_values():
    assert vacuum_env.living_reward == -0.04 
    assert 0 < vacuum_env.discount_factor <= 1
    assert 0 < vacuum_env.learning_rate <= 1
    assert 0 <= vacuum_env.epsilon <= 1
    print("test_values passed")


if __name__ == "__main__":
    test_values()