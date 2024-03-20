#!/usr/bin/python3

"""Unit tests for the State class"""

from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """Unit tests for the State class"""

    def __init__(self, *args, **kwargs):
        """Initialize test_state"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """Test if name attribute is of type string"""
        new = self.value()
        self.assertEqual(type(new.name), str)
