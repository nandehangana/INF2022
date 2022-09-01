# Import the pytest package
import pytest

# Import create_engine() from the main.py module
from main import create_engine

# Complete the unit test name by adding a prefix
def test_on_string_with_one_comma():
  # Complete the assert statement
  assert convert_to_int("2,081") == 2081