from filled_node import get_filled_node
from question_generate import question_generate
from primitives import primitive
from config import config


hidden_f = { }
for idx, x in enumerate(primitive):
    hidden_f[x] = f"f{idx}"

if config.convert_symbol == "anom":
    hidden_f = {
        "filter_gt": "filter_lt",
        "top_k": "bottom_k",
        "filter_gt_c": "filter_lt_c",
        "kth_max": "kth_min",
        "sum": "std",
        "count": "unique",
        "kth_argmax": "kth_argmin",
        "hop": "join",
        "add": "sub",
        "add_c": "sub_c"
    }

if config.convert_symbol == "cross":
    hidden_f = {
        "filter_gt": "add_c",
        "top_k": "add",
        "filter_gt_c": "hop",
        "kth_max": "kth_argmax",
        "sum": "count",
        "count": "sum",
        "kth_argmax": "kth_max",
        "hop": "filter_gt_c",
        "add": "top_k",
        "add_c": "filter_gt"
    }


def hide(node, step):
    assert node in step
    step = step.replace(node, hidden_f[node])
    return step


def get_output(nodes, f_nodes):
    return "; ".join([hide(y, x.reasoning_step) for x, y in zip(f_nodes, nodes)]) \
        + f"; result := {f_nodes[-1].symbol};"


def convert_to_one(output):
    exprs = output.split(";")
    assigned = { }
    for e in exprs:
        e = e.split(":=")
        if len(e) < 2:
            continue
        left = e[0].strip( )
        right = e[1].strip( )
        for x in assigned:
            right = right.replace(x, assigned[x])
        assigned[left] = right
    if "result" not in assigned:
        return None
    else:
        return assigned["result"].replace(' ', '')


def dfs(step, n, dicts, right, candi):
    if step == n:
        candi.append(right)
        return
    k, values = dicts[step]
    if k in right:
        for v in values:
            dfs(step + 1, n, dicts, right.replace(k, v), candi)
    else:
        dfs(step + 1, n, dicts, right, candi)


def get_candidate(assigned, right):
    dicts = [ ]
    for x in assigned:
        dicts.append((x, assigned[x]))
    n, candi = len(dicts), [ ]
    dfs(0, n, dicts, right, candi)
    return candi


def complete_convert_to_one(output):
    exprs = output.split(";")
    assigned = { }
    for e in exprs:
        e = e.split(":=")
        if len(e) < 2:
            continue
        left = e[0].strip( )
        right = e[1].strip( )
        candi = get_candidate(assigned, right)
        if f"{hidden_f['add']} " in right:
            l, r, c = right.find('('), right.find(')'), right.find(',')
            # swap content before and after ','
            right = f"{right[:l]}({right[c + 1:r]},{right[l + 1:c]}){right[r + 1:]}"
            candi += get_candidate(assigned, right)
        assigned[left] = candi
    if "result" not in assigned:
        return None
    return assigned["result"]


class reasoning_sample:
    def __init__(self, graph):
        g_n = graph.n
        nodes = graph.nodes
        reps = graph.reps
        f_nodes = [ ]
        out_cnt = { }
        for x in graph.out_tp:
            out_cnt[x] = 1
        while True:
            size = 1000
            for i in range(g_n):
                rep = reps[i]
                rep = [f_nodes[j].symbol if j != -1 else None for j in rep]
                out_tp = graph.out_tp[i]
                name = f"{out_tp}_{out_cnt[out_tp]}"
                out_cnt[out_tp] += 1
                ret = get_filled_node(nodes[i], rep, name, size)
                if hasattr(ret, "not_filled"):
                    break
                if nodes[i] == "top_k":
                    size = ret.k
                f_nodes.append(ret)
            else:
                break

        self.question = question_generate(graph, f_nodes)
        self.output_steps = get_output(nodes, f_nodes)
        exprs = complete_convert_to_one(self.output_steps)
        self.output_expr = exprs[0]
        self.candi_outputs = [x.replace(' ', '') for x in exprs]

        conv_nodes = [""] * g_n
        for i in range(g_n):
            if nodes[i] == "filter_gt_c" and "column" in f_nodes[i].reasoning_step:
                conv_nodes[i] = "filter_gt_c_colin"
            elif nodes[i] == "hop" and "row" in f_nodes[i].reasoning_step:
                conv_nodes[i] = "hop_rowin"
            else:
                conv_nodes[i] = nodes[i]

        self.graph = graph
        self.nodes = conv_nodes
