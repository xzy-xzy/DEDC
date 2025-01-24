from random import randint


def random_h( ):
    return f"attr_{randint(1, 1000)}"


def number_to_ord(n):
    if n == 1:
        return ""
    if n % 10 == 1 and n % 100 != 11:
        return f"{n}st"
    if n % 10 == 2 and n % 100 != 12:
        return f"{n}nd"
    if n % 10 == 3 and n % 100 != 13:
        return f"{n}rd"
    return f"{n}th"


def comparison_convert(p):
    if "geq" in p:
        return "greater than or equal to"
    if "leq" in p:
        return "less than or equal to"
    if "neq" in p:
        return "not equal to"
    if "eq" in p:
        return "equal to"
    if "gt" in p:
        return "greater than"
    if "lt" in p:
        return "less than"


class node_filter:
    def __init__(self, p, params, step, size):
        # "filter_eq": {"in": ["view", "header", "value"], "out": "view"}
        view, val = params[0], params[2]
        if view is None:
            view = "all"
        if val is None:
            val = randint(0, 1000)
            self.val = val
        symbol = step
        h = random_h( )
        self.text = comparison_convert(p)

        self.reasoning_step = f"{symbol} := {p} ({view}, {h}, {val})"
        self.h = h
        self.symbol = symbol
        self.link_scope = "among"

    def leaf_scope(self):
        return f"the items that satisfy its {self.h} is {self.text} {self.val} among all items"

    def scope(self, val=None):
        if val is None:
            val = self.val
        return f"the items that satisfy its {self.h} is {self.text} {val}"

    def question(self, val=None):
        if val is None:
            val = self.val
        return f"which items satisfy its {self.h} is {self.text} {val}"


class node_filter_c:
    def __init__(self, p, params, step, size):
        # "filter_eq_c": {"in": ["view", "header", "column"], "out": "view"},
        view, col = params[0], params[2]
        if view is None:
            view = "all"
        if col is None:
            col = random_h( )
            self.col = col
            col = {"symbol": col, "header": col, "text": col}
        symbol = step
        h = random_h( )
        while h == col["header"]:
            h = random_h( )
        self.text = comparison_convert(p)

        self.reasoning_step = f"{symbol} := {p} ({view}, {h}, {col['symbol']})"
        self.symbol = symbol
        self.h = h
        self.link_scope = "among"

    def leaf_scope(self):
        return f"the items that satisfy its {self.h} is {self.text} its {self.col} among all items"

    def scope(self, val=None):
        if val is None:
            val = self.col
        return f"the items that satisfy its {self.h} is {self.text} {val}"

    def question(self, val=None):
        if val is None:
            val = self.col
        return f"which items satisfy its {self.h} is {self.text} {val}"


class node_top_k:
    def __init__(self, p, params, step, size):
        # "top_k": {"in": ["view", "header", "k"], "out": "view"}
        if size < 2:
            self.not_filled = True
            return
        view = params[0]
        if view is None:
            view = "all"
        h = random_h( )
        k = randint(2, size)
        symbol = step
        self.text = "top" if "top" in p else "bottom"

        self.reasoning_step = f"{symbol} := {p} ({view}, {h}, {k})"
        self.symbol = symbol
        self.k = k
        self.h = h
        self.link_scope = "among"

    def leaf_scope(self):
        return f"the {self.text} {self.k} items for {self.h} among all items"

    def scope(self):
        return f"the {self.text} {self.k} items for {self.h}"

    def question(self):
        return f"which are the {self.text} {self.k} items for {self.h}"


class node_kth_max:
    def __init__(self, p, params, step, size):
        # "kth_max": {"in": ["view", "header", "k"], "out": "value"}
        if size < 2:
            self.not_filled = True
            return
        view = params[0]
        if view is None:
            view = "all"
        h = random_h( )
        k = randint(2, size)
        symbol = step
        self.text = "largest" if "max" in p else "smallest"

        self.reasoning_step = f"{symbol} := {p} ({view}, {h}, {k})"
        self.symbol = symbol
        self.h = h
        self.order = number_to_ord(k)
        self.link_scope = "of"

    def leaf_value(self):
        return f"the {self.order} {self.text} {self.h} of all items"

    def value(self):
        return f"the {self.order} {self.text} {self.h}"

    def question(self):
        return f"what is the {self.order} {self.text} {self.h}"


def col_op_convert(p):
    if "avg" in p:
        return "average"
    if "sum" in p:
        return "sum"
    if "var" in p:
        return "variance"
    if "std" in p:
        return "standard deviation"


class node_avg:
    def __init__(self, p, params, step, size):
        # "sum": {"in": ["view", "header"], "out": "value"}
        view = params[0]
        if view is None:
            view = "all"
        h = random_h( )
        symbol = step
        self.text = col_op_convert(p)

        self.reasoning_step = f"{symbol} := {p} ({view}, {h})"
        self.symbol = symbol
        self.h = h
        self.link_scope = "of"

    def leaf_value(self):
        return f"the {self.text} of {self.h} of all items"

    def value(self):
        return f"the {self.text} of {self.h}"

    def question(self):
        return f"what is the {self.text} of {self.h}"


class node_count:
    def __init__(self, p, params, step, size):
        # "count": {"in": ["view"], "out": "value"}
        view = params[0]
        if view is None:
            view = "all"
        symbol = step

        self.reasoning_step = f"{symbol} := count ({view})"
        self.symbol = symbol
        self.link_scope = "of"

    def leaf_value(self):
        return "the number of all items"

    def value(self):
        return "the number"

    def question(self):
        return f"what is the number"


class node_kth_argmax:
    def __init__(self, p, params, step, size):
        # "kth_argmax": {"in": ["view", "header", "k"], "out": "row"}
        if size < 2:
            self.not_filled = True
            return
        view = params[0]
        if view is None:
            view = "all"
        h = random_h( )
        k = randint(2, size)
        symbol = step
        self.text = "largest" if "argmax" in p else "smallest"

        self.reasoning_step = f"{symbol} := {p} ({view}, {h}, {k})"
        self.symbol = symbol
        self.h = h
        self.order = number_to_ord(k)
        self.link_scope = "among"

    def leaf_scope(self):
        return f"the item that has the {self.order} {self.text} {self.h} among all items"

    def scope(self):
        return f"the item that has {self.order} {self.text} {self.h}"

    def question(self):
        return f"which item has the {self.order} {self.text} {self.h}"


class node_hop:
    def __init__(self, p, params, step, size):
        # "hop": {"in": ["row", "header"], "out": "value"}
        row = params[0]
        if row is None:
            row = randint(1, size)
            row = f"item_{row}"
        h = random_h( )
        symbol = step

        self.reasoning_step = f"{symbol} := hop ({row}, {h})"
        self.symbol = symbol
        self.h = h
        self.row = row
        self.link_scope = "of"

    def leaf_value(self):
        return f"the {self.h} of {self.row}"

    def value(self):
        return f"the {self.h}"

    def question(self):
        return f"what is the {self.h}"


def math_op_convert(p):
    if "add" in p:
        return "sum of", "plus"
    if "sub" in p:
        return "difference between", "minus"
    if "mul" in p:
        return "product of", "times"
    if "div" in p:
        return "quotient of", "divided by"


class node_add:
    def __init__(self, p, params, step, size):
        # "add": {"in": ["value", "value"], "out": "value"}
        val1, val2 = params[0], params[1]
        assert val1 is not None or val2 is not None
        if val1 is None:
            val1 = randint(0, 1000)
            self.val1 = val1
        if val2 is None:
            val2 = randint(0, 1000)
            self.val2 = val2

        symbol = step
        self.text, self.op = math_op_convert(p)

        self.reasoning_step = f"{symbol} := {p} ({val1}, {val2})"
        self.symbol = symbol

    def value(self, val, val2=None):
        if val2 is None:
            value1, value2 = val, self.val2
        else:
            value1, value2 = val, val2
        return f"{value1} {self.op} {value2}"

    def question(self, val, val2=None):
        if val2 is None:
            value1, value2 = val, self.val2
        else:
            value1, value2 = val, val2
        return f"what is {value1} {self.op} {value2}"


class node_add_c:
    def __init__(self, p, params, step, size):
        # "add_c": {"in": ["header", "value"], "out": "column"},
        val = params[1]
        h = random_h( )
        if val is None:
            val = randint(0, 1000)
            self.val = val
        symbol = step
        self.text, self.op = math_op_convert(p)

        self.reasoning_step = f"{symbol} := {p} ({h}, {val})"
        self.symbol = {"symbol": symbol, "header": h, "text": f"the {self.text} {h} and {val}"}

    def leaf_value(self):
        return f"its {self.symbol['header']} {self.op} {self.val}"

    def value(self, val=None):
        if val is None:
            val = self.val
        return f"its {self.symbol['header']} {self.op} {val}"



index = {
    "filter_gt": node_filter,
    "filter_l": node_filter,
    "filter_geq": node_filter,
    "filter_leq": node_filter,
    "filter_eq": node_filter,
    "filter_neq": node_filter,
    "filter_gt_c": node_filter_c,
    "filter_l_c": node_filter_c,
    "filter_geq_c": node_filter_c,
    "filter_leq_c": node_filter_c,
    "filter_eq_c": node_filter_c,
    "filter_neq_c": node_filter_c,
    "add_c": node_add_c,
    "sub_c": node_add_c,
    "mul_c": node_add_c,
    "div_c": node_add_c,
    "top_k": node_top_k,
    "bottom_k": node_top_k,
    "kth_max": node_kth_max,
    "kth_min": node_kth_max,
    "avg": node_avg,
    "sum": node_avg,
    "var": node_avg,
    "std": node_avg,
    "count": node_count,
    "kth_argmax": node_kth_argmax,
    "kth_argmin": node_kth_argmax,
    "hop": node_hop,
    "add": node_add,
    "sub": node_add,
    "mul": node_add,
    "div": node_add,
}


def get_filled_node(p, params, step, size):
    return index[p](p, params, step, size)
