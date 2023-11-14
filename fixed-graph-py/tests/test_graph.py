# -*- coding: utf-8 -*-
# Unit test module for the Builder class.


import pytest
import unittest
from src.graph import Builder, Node


class UnitTestsForBuilder(unittest.TestCase):
    def setUp(self):
        """Set up the test fixture."""

        self.builder = Builder()
        self.builder.init()

    def test_instantiation(self):
        """Test instantiation and initial conditions of Builder class."""

        self.assertIsInstance(self.builder, Builder)
        self.assertIsNotNone(self.builder.root)
        self.assertIsNone(self.builder.graph_evaluation)
        self.assertEqual(self.builder.equality_constraints, [])

    def test_private_methods_general(self):
        """Test general private methods of Builder class."""

        self.assertFalse(self.builder._is_filled)
        self.assertEqual(self.builder._create_node(), Node())
        self.assertTrue(self.builder._is_graph_free_of_constraints())

    def test_private_methods_parsing_addition(self):
        """Test private methods of Builder class related to addition."""

        node_add = Node(addition=[Node(val=1), Node(val=2)])
        self.assertEqual(self.builder._parse_addition_node(node_add), 3)

        node_add = Node(addition=[Node(val=0), Node(val=0)])
        self.assertEqual(self.builder._parse_addition_node(node_add), 0)

        node_add = Node(addition=[Node(val=1), None])
        with pytest.raises(SystemExit):
            self.builder._parse_addition_node(node_add)

    def test_private_methods_parsing_multiplication(self):
        """Test private methods of Builder class related to multiplication."""

        node_mul = Node(multiplication=[Node(val=1), Node(val=2)])
        self.assertEqual(self.builder._parse_multiplication_node(node_mul), 2)

        node_mul = Node(multiplication=[Node(val=0), Node(val=0)])
        self.assertEqual(self.builder._parse_multiplication_node(node_mul), 0)

        node_mul = Node(multiplication=[Node(val=1), None])
        with pytest.raises(SystemExit):
            self.builder._parse_multiplication_node(node_mul)

    def test_private_methods_parsing_equality(self):
        """Test private methods of Builder class related to equality."""

        self.assertEqual(self.builder.equality_constraints, [])
        node_eq = Node(equality=Node(val=1))
        self.assertEqual(self.builder._parse_equality_node(node_eq), 1)
        self.assertEqual(self.builder.equality_constraints, [[node_eq, None]])

    def test_init(self):
        """Test the public method init()."""

        self.assertTrue(self.builder.root.is_input)
        self.assertIsInstance(self.builder.root, Node)

    def test_constant(self):
        """Test the public method constant()."""

        node = self.builder.constant(1)
        self.assertTrue(node.is_constant)
        self.assertEqual(node.val, 1)

    def test_add(self):
        """Test the public method add()."""

        node1 = self.builder.constant(1)
        node2 = self.builder.constant(2)
        node_add = self.builder.add(node1, node2)
        self.assertTrue(node_add.addition, [node1, node2])
        self.assertIsNone(node_add.val)

    def test_mul(self):
        """Test the public method mul()."""

        node1 = self.builder.constant(1)
        node2 = self.builder.constant(2)
        node_mul = self.builder.mul(node1, node2)
        self.assertTrue(node_mul.multiplication, [node1, node2])
        self.assertIsNone(node_mul.val)

    def test_eq(self):
        """Test the public method eq()."""

        node = self.builder.constant(1)
        node_eq = self.builder.equal(node)
        self.assertTrue(node_eq.equality, node)
        self.assertIsNone(node_eq.val)

    def test_assert_equal(self):
        """Test the public method assert_equal()."""

        node1 = self.builder.constant(1)
        node2 = self.builder.constant(2)

        self.assertFalse(self.builder.assert_equal(node1, node2))
        self.assertTrue(self.builder.assert_equal(node1, node1))

        with pytest.raises(SystemExit):
            self.builder._parse_addition_node(None)

    def test_fill_nodes(self):
        """Test the public method fill_nodes()."""

        self.assertFalse(self.builder._is_filled)
        self.builder.fill_nodes(5)
        self.assertEqual(self.builder.root.val, 5)
        self.assertTrue(self.builder._is_filled)
        self.assertEqual(self.builder.graph_evaluation, 5)

    def test_check_constraints(self):
        """Test the public method check_constraints()."""

        self.assertEqual(self.builder.graph_evaluation, None)
        with pytest.raises(SystemExit):
            self.builder.check_constraints()

        self.builder.fill_nodes(5)
        self.builder.check_constraints()
        self.assertEqual(self.builder.graph_evaluation, 5)

    def test_get_last_constrained_node(self):
        """Test the public method get_last_constrained_node()."""

        with pytest.raises(SystemExit):
            self.builder.get_last_constrained_node()

        node = self.builder.constant(1)
        self.builder.equality_constraints = [node]
        self.assertEqual(self.builder.get_last_constrained_node(), node)
