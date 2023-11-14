# -*- encoding: utf-8 -*-
# Classes to create fixed computational graphs.

from dataclasses import dataclass
from src.utils import log_debug, log_error, log_info, exit_with_error


@dataclass
class Node:
    """Define a node data type, including its type of node and any data."""

    is_input: bool = False
    is_constant: bool = False
    equality: str = None
    addition: list = None
    multiplication: list = None
    val: float = None
    next_node: str = None


class Builder:
    """Builder class for a fixed computational graph."""

    def __init__(self):
        self.root = None
        self.graph_evaluation: float = None
        self.equality_constraints: list = []

    ##################################
    #      Private methods: General
    ##################################
    @property
    def _is_filled(self) -> bool:
        """Check if the graph is filled."""

        return self.graph_evaluation is not None

    @staticmethod
    def _create_node(
        is_input: bool = False,
        is_constant: bool = False,
        val: float = None,
        multiplication: list = None,
        addition: list = None,
        equality: str = None,
    ) -> Node:
        """Initializes a new node to be added to the graph."""

        return Node(
            is_input=is_input,
            is_constant=is_constant,
            val=val,
            multiplication=multiplication,
            addition=addition,
            equality=equality,
        )

    @staticmethod
    def _get_memory_address(node: Node) -> str:
        """Get the memory address of a node."""

        return hex(id(node))

    def _is_graph_free_of_constraints(self) -> bool:
        """Check that there are no constrained values left."""

        if self.equality_constraints == []:
            return True

        for pair in self.equality_constraints:
            try:
                if pair[1] is None:
                    return False
            except IndexError:
                exit_with_error("Equality constraints array is not properly formatted.")

        return True

    def _get_last_node(self) -> Node:
        """Find the next position in the graph."""

        this_node = self.root
        if this_node is None:
            exit_with_error(
                f"Graph at {self._get_graph_address()} has no root. Initialize it before adding nodes"
            )
        while this_node.next_node is not None:
            prev_node = this_node
            this_node = this_node.next_node

        return this_node

    def _get_graph_address(self) -> str:
        """Get the memory address of the graph, defined by the root node."""

        return self._get_memory_address(self.root)

    def _set_graph_evaluation(self, result) -> None:
        """Add the result of the graph to the builder."""

        self.graph_evaluation = result
        self.check_constraints()
        log_debug(f"Finished filling nodes for graph at {self._get_graph_address()}")

    def _print_graph_evaluation(self) -> None:
        """Get the result of the graph."""

        log_info(f"RESULT: {self.graph_evaluation}\n")

    ##################################
    #      Private methods: Parsing
    ##################################
    def _parse_addition_node(self, this_node: Node) -> float:
        """Parse the addition node."""

        try:
            this_node.val = this_node.addition[0].val + this_node.addition[1].val
            log_info(
                f"→ Found addition: {this_node.addition[0].val} + {this_node.addition[1].val} = {this_node.val}"
            )
        except (TypeError, AttributeError):
            exit_with_error(
                f"Addition node {this_node} is not initialized. Initialize it before filling the graph"
            )
        return this_node.val

    def _parse_multiplication_node(self, this_node: Node) -> float:
        """Parse the multiplication node."""

        try:
            this_node.val = (
                this_node.multiplication[0].val * this_node.multiplication[1].val
            )
            log_info(
                f"→ Found multiplication: {this_node.multiplication[0].val} * {this_node.multiplication[1].val} = {this_node.val}"
            )
        except (TypeError, AttributeError):
            exit_with_error(
                f"Multiplication node {this_node} is not initialized. Initialize it before filling the graph"
            )
        return this_node.val

    def _parse_equality_node(self, this_node: Node) -> float:
        """Parse the equality node."""

        this_node.val = this_node.equality.val
        self.equality_constraints.append([this_node, None])

        log_info(f"→ Found equality: exiting at constrained node val={this_node.val}")
        return this_node.val

    ##############################
    #      Public methods
    ##############################
    def init(self) -> Node:
        """Initialize the root of the graph (an input node is a node with no parents)"""

        self.root = self._create_node(is_input=True)
        log_debug(f"New graph created with root node at {self._get_graph_address()}")
        return self.root

    def constant(self, val: float) -> Node:
        """Create a constant node."""

        new_node = self._create_node(is_constant=True, val=val)
        position = self._get_last_node()
        position.next_node = new_node

        log_debug(
            f"Constant node with val={val} created at {self._get_memory_address(new_node)}"
        )

        return new_node

    def mul(self, node_x: Node, node_y: Node) -> Node:
        """Create a multiplication node."""

        new_node = self._create_node(multiplication=[node_x, node_y])
        position = self._get_last_node()
        position.next_node = new_node

        nodes_addresses = [
            self._get_memory_address(node_x),
            self._get_memory_address(node_y),
        ]
        log_debug(
            f"Multiplication node for {nodes_addresses} created at {self._get_memory_address(new_node)}"
        )

        return new_node

    def add(self, node_x: Node, node_y: Node) -> Node:
        """Create an addition node."""

        new_node = self._create_node(addition=[node_x, node_y])
        position = self._get_last_node()
        position.next_node = new_node

        nodes_addresses = [
            self._get_memory_address(node_x),
            self._get_memory_address(node_y),
        ]
        log_debug(
            f"Addition node for {nodes_addresses} created at {self._get_memory_address(new_node)}"
        )

        return new_node

    def equal(self, node: Node) -> Node:
        """Create an equality node."""

        new_node = self._create_node(equality=node)
        position = self._get_last_node()
        position.next_node = new_node

        log_debug(
            f"Equality node for {self._get_memory_address(node)} created at {self._get_memory_address(new_node)}"
        )

        return new_node

    def assert_equal(self, node_x: Node, node_y: Node) -> bool:
        """Assert that two given nodes are equal under the constraints of the graph."""

        if node_x is None or node_y is None:
            exit_with_error(
                "Can't assert equality between constrained nodes as one of them is None"
            )
        elif node_x.val != node_y.val:
            log_error(
                f"Nodes {self._get_memory_address(node_x)} and {self._get_memory_address(node_y)} are not equal."
            )
            return False
        else:
            log_debug(
                f"Nodes {self._get_memory_address(node_x)} and {self._get_memory_address(node_y)} are equal with val={node_x.val}"
            )
            return True

    def fill_nodes(self, val: int) -> None:
        """Fill the nodes of the graph with an input value."""

        log_debug(f"Starting filling nodes with x={val}")

        self.root.val = val
        this_node = self.root
        prev_node = None

        while this_node is not None:

            if this_node.is_input:
                this_node.val = val

            elif this_node.addition is not None:
                self._parse_addition_node(this_node)

            elif this_node.multiplication is not None:
                self._parse_multiplication_node(this_node)

            elif this_node.equality is not None:
                self._parse_equality_node(this_node)

            elif this_node.is_constant is not None:
                log_info(f"→ Found constant: {this_node.val}")

            else:
                exit_with_error(f"Node type is not supported")

            prev_node = this_node
            this_node = this_node.next_node

        if self._is_graph_free_of_constraints():
            self._set_graph_evaluation(prev_node.val)
            self._print_graph_evaluation()

    def check_constraints(self) -> None:
        """Check that the constraints of the graph are met."""

        if not self._is_filled:
            exit_with_error("Graph is not filled. Fill it before checking constraints")

        for pair in self.equality_constraints:
            try:
                self.assert_equal(pair[0], pair[1])
                log_info("All constraints were met")
            except (AssertionError, TypeError):
                exit_with_error("Not all constraints were met")

    def get_last_constrained_node(self) -> float:
        """
        Get the last constrained node from the list of all constrained nodes
        contained in the graph, so that it can be used to generate the hinted graph.
        """
        log_debug(
            f"Getting last constrained node from graph at {self._get_graph_address()}"
        )
        try:
            return self.equality_constraints[-1]
        except IndexError:
            exit_with_error(
                f"Graph at {self._get_graph_address()} has no constraints. Add constraints before getting the last one"
            )

    def update_with_hint(self, equality_node: Node) -> None:
        """Update the original graph with the sub-graph generated with the hint."""

        try:
            self.equality_constraints[0][0].next_node = equality_node
            self.equality_constraints[0][1] = equality_node
            self._set_graph_evaluation(equality_node.val)
            self._print_graph_evaluation()
        except IndexError:
            exit_with_error(
                f"Graph at {self._get_graph_address()} has no constraints. Add constraints before updating with a hint"
            )
