# Import the pytest package
import pytest

# Import getICsAndWeights() from the main.py module
from app.weights_and_ics import getICsAndWeights

# Complete the unit test name by adding a prefix
def test_on_string_with_one_comma():
  # Complete the assert statement
  assert convert_to_int("2,081") == 2081