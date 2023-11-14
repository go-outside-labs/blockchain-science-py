# -*- coding: utf-8 -*-
# Example of functions expressed as fixed computational graph with hints.
# Note: this class is not meant to be instantiated and it's designed to be
# used as script destination for example functions.

from src.graph import Builder
from src.utils import log_info, log_error, log_debug


def quadratic(val: int = 3) -> None:
    """
    Run for f(x) = x^2 + 5 + x.
    For instance, if x = 3, f(3) = 17.
    """

    log_info(f"CALCULATING: f(x) = x^2 + 5 + x, x = {val}")

    # Initialize the graph
    builder = Builder()
    x = builder.init()

    # Build nodes
    x_squared = builder.mul(x, x)
    five = builder.constant(5)
    x_squared_plus_5 = builder.add(x_squared, five)
    _ = builder.add(x_squared_plus_5, x)

    # Evaluate the graph
    builder.fill_nodes(val)


def cubic(val: int = 5) -> None:
    """
    Run for f(x) = x^3 + x^2 + 2x + 3.
    For instance, if x = 5, f(2) = 19.
    """

    log_info(f"CALCULATING: f(x) = x^3 + x^2 + 2x + 3, x = {val}:")

    # Initialize the graph
    builder = Builder()
    x = builder.init()

    # Build nodes
    x_squared = builder.mul(x, x)
    x_cubed = builder.mul(x_squared, x)
    x_cubed_plus_x_squared = builder.add(x_squared, x_cubed)
    two = builder.constant(2)
    x_times_two = builder.mul(x, two)
    x_squared_plus_x_cubed_plus_2x = builder.add(x_cubed_plus_x_squared, x_times_two)
    three = builder.constant(3)
    _ = builder.add(x_squared_plus_x_cubed_plus_2x, three)

    # Evaluate the graph
    builder.fill_nodes(val)


def hint_for_division(val: int = 3) -> None:
    """
    Run for f(x) = 8 / (x + 1).
    For instance, if x = 3, f(3) = 32, wih constraint node b = 4.
    Note the graphs could be generated asynchronously.
    """

    log_info(f"CALCULATING: f(x) = 8 / (x + 1), x = {val}:")

    # FIRST THREAD
    # Initialize the graph
    builder = Builder()
    x = builder.init()

    # Build nodes from the left up to the equal sign (constrained node)
    constant_1 = builder.constant(1)
    x_plus_1 = builder.add(x, constant_1)
    b = builder.equal(x_plus_1)

    # SECOND THREAD
    # Initialize the second graph
    second_builder = Builder()
    c = second_builder.init()

    # Build nodes from the right up to the equal sign (hinted node)
    constant_8 = second_builder.constant(8)
    _ = second_builder.mul(c, constant_8)

    # AFTER THE END OF THE FIRST THREAD
    # Evaluate the graph
    builder.fill_nodes(val)

    # AFTER THE END OF THE FIRST AND SECOND THREAD
    # Evaluate the second graph with the value at the constrained node (b)
    constrained_node, _ = builder.get_last_constrained_node()
    second_builder.fill_nodes(constrained_node.val)
    builder.update_with_hint(second_builder.root)
