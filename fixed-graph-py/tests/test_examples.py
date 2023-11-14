# -*- coding: utf-8 -*-
# End-to-end tests for polynomial equations.

import pytest
import unittest
from src.graph import Builder, Node


class PolynomialTests(unittest.TestCase):
    def setUp(self):
        """Set up the test fixture."""

        self.builder = Builder()
        self.another_builder = Builder()

        self.x = self.builder.init()
        self.c = self.another_builder.init()
        self.x_squared = self.builder.mul(self.x, self.x)
        self.x_cubed = self.builder.mul(self.x_squared, self.x)

        self.one = self.builder.constant(1)
        self.two = self.builder.constant(2)
        self.three = self.builder.constant(3)
        self.five = self.builder.constant(5)
        self.eight = self.builder.constant(8)

    def test_quadratic(self):
        """Test the public method quadratic()."""

        x_squared_plus_5 = self.builder.add(self.x_squared, self.five)
        _ = self.builder.add(x_squared_plus_5, self.x)

        self.builder.fill_nodes(3)

        self.assertEqual(self.builder.graph_evaluation, 17)
        self.assertTrue(self.builder._is_graph_free_of_constraints())

    def test_cubic(self):
        """Test the public method cubic()."""

        x_cubed_plus_x_squared = self.builder.add(self.x_squared, self.x_cubed)
        x_times_two = self.builder.mul(self.x, self.two)
        x_squared_plus_x_cubed_plus_2x = self.builder.add(
            x_cubed_plus_x_squared, x_times_two
        )
        _ = self.builder.add(x_squared_plus_x_cubed_plus_2x, self.three)

        self.builder.fill_nodes(5)

        self.assertEqual(self.builder.graph_evaluation, 163)

    def test_hint_example(self):
        """Test the public method hint_example()."""

        x_plus_1 = self.builder.add(self.x, self.one)
        b = self.builder.equal(x_plus_1)

        # Test the first builder after filling its nodes
        self.builder.fill_nodes(3)
        self.assertEqual(self.builder.root.val, 3)
        self.assertIsNone(self.builder.graph_evaluation)
        self.assertEqual(self.builder.equality_constraints[0][0].val, 4)
        self.assertIsNone(self.builder.equality_constraints[0][1])

        # Test the second builder before filling its nodes
        _ = self.another_builder.mul(self.c, self.eight)
        constrained_node, _ = self.builder.get_last_constrained_node()
        self.assertEqual(constrained_node.val, 4)

        # Test the second builder after filling its nodes
        self.another_builder.fill_nodes(constrained_node.val)
        self.assertEqual(self.another_builder.root.val, constrained_node.val)
        self.assertIsNone(self.builder.graph_evaluation)
        self.assertEqual(self.builder.equality_constraints[0][0].val, 4)
        self.assertEqual(self.another_builder.graph_evaluation, 32)

        # Test the first builder after updating it with the second builder
        self.builder.update_with_hint(self.another_builder.root)
        self.assertEqual(self.builder.graph_evaluation, 4)
        self.assertTrue(self.builder._is_graph_free_of_constraints())
        self.assertEqual(
            self.builder.equality_constraints[0][0].val,
            self.builder.equality_constraints[0][1].val,
        )
        self.assertTrue(
            self.builder.assert_equal(
                self.builder.equality_constraints[0][0],
                self.builder.equality_constraints[0][1],
            )
        )
