""" Implement the hello command.

"""
from ..core.logger import logger


def main(name="World") -> int:
    """ Execute the command.
    
    :param name: name to use in greeting
    """
    logger.debug("executing hello command")
    print(f'Hello, {name}!')
    return 0
