""" Application commands common to all interfaces.

"""
from .hello import main as hello
from .generate import main as generate

__all__ = "hello", "generate"
