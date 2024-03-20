#!/usr/bin/python3

"""Unit tests for the Review class"""

from tests.test_models.test_base_model import test_basemodel
from models.review import Review


class test_review(test_basemodel):
    """Unit tests for the Review class"""

    def __init__(self, *args, **kwargs):
        """Initialize test_review"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """Test if place_id attribute is of type string"""
        new = self.value()
        self.assertEqual(type(new.place_id), str)

    def test_user_id(self):
        """Test if user_id attribute is of type string"""
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """Test if text attribute is of type string"""
        new = self.value()
        self.assertEqual(type(new.text), str)
