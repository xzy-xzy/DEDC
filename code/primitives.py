primitive = {
    "filter_gt": {"in": ["view", "header", "value"], "out": "view"},    # f0
    "top_k": {"in": ["view", "header", "k"], "out": "view"},    # f1
    "filter_gt_c": {"in": ["view", "header", "column"], "out": "view"},   # f2
    "kth_max": {"in": ["view", "header", "k"], "out": "value"},   # f3
    "sum": {"in": ["view", "header"], "out": "value"},  # f4
    "count": {"in": ["view"], "out": "value"},  # f5
    "kth_argmax": {"in": ["view", "header", "k"], "out": "row"},    # f6
    "hop": {"in": ["row", "header"], "out": "value"},   # f7
    "add": {"in": ["value", "value"], "out": "value"},      # f8
    "add_c": {"in": ["header", "value"], "out": "column"},  # f9
}

math_op = {"add", "sub", "mul", "div"}
math_c_op = {"add_c"}


out_ord = {
    "view": 0,
    "value": 1,
    "row": 2,
    "column": 3,
}