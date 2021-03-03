import pytest
from src.greeting import greeting


class TestGreeting:
    def test_greeting(self):
        result = greeting("Welcome to Pythonic!")
        expected_result = "Hi, Welcome to Pythonic!"
        assert result == expected_result