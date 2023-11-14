## prototyping a fixed computational graph

<br>

a high-level way of thinking about zero-knowledge proofs is to prove a statement where:

> a function `f` evaluated at inputs `x_i` results in an output `(y_1,...,y_n)`, i.e., `f(x_1, ..., x_n) = (y_1, ..., y_n)`. 


this function can be expressed as a fixed computational graph, where nodes are integers and relationships between nodes are related by operations such as **multiplication or addition relationships**. this graph defines a symbolic graph, which is filled in a later operation. 

in addition, some nodes can be related to others with an **equality relationship** on which the node's value is computed outside of the graph and constrained by a **hint**.




<br>

---

### setting up

<br>


```bash
➜ tree .
.
├── Makefile
├── README.md
├── pyproject.toml
├── src
│   ├── __init__.py
│   ├── examples.py
│   ├── graph.py
│   ├── main.py
│   └── utils.py
├── tests
│   ├── __init__.py
│   ├── test_examples.py
│   └── test_graph.py
└── tox.ini
```

<br>

this project utilizes [poetry](https://python-poetry.org/docs/) to set a customized virtual environment and installation:



```bash
➜ brew install poetry
➜ make install
```

<br>

configuration details can be found at `pyproject.toml`. in addition, an `.env` file should be created, and the logging level should be set to its environment variable:


```bash
➜ cp .env_example .env
➜ vim .env
```

<br>

note that even though the project has only one environment variable, this design choice is the most appropriate for production code.

<br>

--- 

### running examples without constraints

<br>

two examples of quadratic and cubic polynomial equations are illustrated in `src/examples.py`, and can be run with `LOG_LEVEL=debug` as follows:

```bash
➜ make example

✅ CALCULATING: f(x) = x^2 + 5 + x, x = 3
🟨 New graph created with root node at 0x102fb2960
🟨 Multiplication node for ['0x102fb2960', '0x102fb2960'] created at 0x102fb28a0
🟨 Constant node with val=5 created at 0x102fb29f0
🟨 Addition node for ['0x102fb28a0', '0x102fb29f0'] created at 0x102fb2a20
🟨 Addition node for ['0x102fb2a20', '0x102fb2960'] created at 0x102fb2840
🟨 Starting filling nodes with x=3
✅ → Found multiplication: 3 * 3 = 9
✅ → Found constant: 5
✅ → Found addition: 9 + 5 = 14
✅ → Found addition: 14 + 3 = 17
🟨 Finished filling nodes for graph at 0x102fb2960
✅ RESULT: 17

✅ CALCULATING: f(x) = x^3 + x^2 + 2x + 3, x = 5:
🟨 New graph created with root node at 0x102fb2a50
🟨 Multiplication node for ['0x102fb2a50', '0x102fb2a50'] created at 0x102fb2900
🟨 Multiplication node for ['0x102fb2900', '0x102fb2a50'] created at 0x102fb29c0
🟨 Addition node for ['0x102fb2900', '0x102fb29c0'] created at 0x102fb2990
🟨 Constant node with val=2 created at 0x102fb28d0
🟨 Multiplication node for ['0x102fb2a50', '0x102fb28d0'] created at 0x102fb27b0
🟨 Addition node for ['0x102fb2990', '0x102fb27b0'] created at 0x102fb2a80
🟨 Constant node with val=3 created at 0x102fb2b70
🟨 Addition node for ['0x102fb2a80', '0x102fb2b70'] created at 0x102fb2b40
🟨 Starting filling nodes with x=5
✅ → Found multiplication: 5 * 5 = 25
✅ → Found multiplication: 25 * 5 = 125
✅ → Found addition: 25 + 125 = 150
✅ → Found constant: 2
✅ → Found multiplication: 5 * 2 = 10
✅ → Found addition: 150 + 10 = 160
✅ → Found constant: 3
✅ → Found addition: 160 + 3 = 163
🟨 Finished filling nodes for graph at 0x102fb2a50
✅ RESULT: 163
```

<br>

or, with `LOG_LEVEL=info`:

```bash
✅ CALCULATING: f(x) = x^2 + 5 + x, x = 3
✅ → Found multiplication: 3 * 3 = 9
✅ → Found constant: 5
✅ → Found addition: 9 + 5 = 14
✅ → Found addition: 14 + 3 = 17
✅ RESULT: 17

✅ CALCULATING: f(x) = x^3 + x^2 + 2x + 3, x = 5:
✅ → Found multiplication: 5 * 5 = 25
✅ → Found multiplication: 25 * 5 = 125
✅ → Found addition: 25 + 125 = 150
✅ → Found constant: 2
✅ → Found multiplication: 5 * 2 = 10
✅ → Found addition: 150 + 10 = 160
✅ → Found constant: 3
✅ → Found addition: 160 + 3 = 163
✅ RESULT: 163
```

<br>

---

### running examples with constraints

<br>


a simple API (starter) to `hint` arbitrary nodes is available, and it natively supports asynchronous hints and support for parallelization for filling the graph.

an example is illustrated at `src/examples.py`, which can be run with `LOG_LEVEL=debug`:


```bash
➜ make api

✅ CALCULATING: f(x) = 8 / (x + 1), x = 3:
🟨 New graph created with root node at 0x100f5a960
🟨 Constant node with val=1 created at 0x100f5a8a0
🟨 Addition node for ['0x100f5a960', '0x100f5a8a0'] created at 0x100f5a9f0
🟨 Equality node for 0x100f5a9f0 created at 0x100f5aa20
🟨 New graph created with root node at 0x100f5a900
🟨 Constant node with val=8 created at 0x100f5a9c0
🟨 Multiplication node for ['0x100f5a900', '0x100f5a9c0'] created at 0x100f5a990
🟨 Starting filling nodes with x=3
✅ → Found constant: 1
✅ → Found addition: 3 + 1 = 4
✅ → Found equality: exiting at constrained node val=4
🟨 Getting last constrained node from graph at 0x100f5a960
🟨 Starting filling nodes with x=4
✅ → Found constant: 8
✅ → Found multiplication: 4 * 8 = 32
🟨 Finished filling nodes for graph at 0x100f5a900
✅ RESULT: 32

🟨 Nodes 0x100842990 and 0x100842840 are equal with val=4
✅ All constraints were met
🟨 Finished filling nodes for graph at 0x100842ab0
✅ RESULT: 4
```

<br>

or, with `LOG_LEVEL=info`:

```bash
✅ CALCULATING: f(x) = 8 / (x + 1), x = 3:
✅ → Found constant: 1
✅ → Found addition: 3 + 1 = 4
✅ → Found equality: exiting at constrained node val=4
✅ → Found constant: 8
✅ → Found multiplication: 4 * 8 = 32
✅ RESULT: 32

✅ All constraints were met
✅ RESULT: 4
```

<br>

in addition, the examples above are also wrapped with a CLI tool, which could be run with: 

```
➜  python src/main.py
usage: main.py [-h] [-e] [-a]

👾 Fixed Computational Graph Example 👾

options:
  -h, --help  show this help message and exit
  -e          Run examples for quadratic and cubic polynomial functions.
  -a          Run an example that utilizes a hint for a constrained none.
```

<br>

Once again, this design choice was picked to enhance the project's characteristics of production code. For instance, it would be straightforward to extend this CLI tool to accept hint inputs for arbitrary nodes, and to create visual graph plots based on the node type at `Node()`, among other features.

<br>

--- 

### Running tests

<br>

Unit tests for the main classes (`graph.py` and `examples.py`), including edge cases, can be tested with:

```bash
➜ make test

======================================== test session starts ===============================

collected 17 items
tests/test_examples.py::PolynomialTests::test_cubic PASSED                             [  5%]
tests/test_examples.py::PolynomialTests::test_hint_example PASSED                      [ 11%]
tests/test_examples.py::PolynomialTests::test_quadratic PASSED                         [ 17%]
tests/test_graph.py::UnitTestsForBuilder::test_add PASSED                              [ 23%]
tests/test_graph.py::UnitTestsForBuilder::test_assert_equal PASSED                     [ 29%]
tests/test_graph.py::UnitTestsForBuilder::test_check_constraints PASSED                [ 35%]
tests/test_graph.py::UnitTestsForBuilder::test_constant PASSED                         [ 41%]
tests/test_graph.py::UnitTestsForBuilder::test_eq PASSED                               [ 47%]
tests/test_graph.py::UnitTestsForBuilder::test_fill_nodes PASSED                       [ 52%]
tests/test_graph.py::UnitTestsForBuilder::test_get_last_constrained_node PASSED        [ 58%]
tests/test_graph.py::UnitTestsForBuilder::test_init PASSED                             [ 64%]
tests/test_graph.py::UnitTestsForBuilder::test_instantiation PASSED                    [ 70%]
tests/test_graph.py::UnitTestsForBuilder::test_mul PASSED                              [ 76%]
tests/test_graph.py::UnitTestsForBuilder::test_private_methods_general PASSED          [ 82%]
tests/test_graph.py::UnitTestsForBuilder::test_private_methods_parsing_addition PASSED [ 88%]
tests/test_graph.py::UnitTestsForBuilder::test_private_methods_parsing_equality PASSED [ 94%]
tests/test_graph.py::UnitTestsForBuilder::test_private_methods_parsing_mul PASSED      [100%]

===================================== 17 passed in 0.01s ===============================
```

<br>

--- 

### developing


<br>

development resources such as lint and cleaning the language's cache are available with:

```bash
➜ make lint
➜ make clean
```
