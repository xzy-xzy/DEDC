from primitives import primitive, out_ord, math_op, math_c_op


class base_graph:
    def __init__(self, prev, idx):
        self.prev = prev
        self.idx = idx
        self.n = len(prev)
        succ = [[ ] for _ in range(self.n)]
        for x in prev:
            for y in prev[x]:
                succ[y].append(x)
        self.succ = succ
        self.filled = [ ]

    def check_isomorphism(self, nodes):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.prev[i] == self.prev[j] and self.succ[i] == self.succ[j]:
                    if out_ord[primitive[nodes[i]]["out"]] > out_ord[primitive[nodes[j]]["out"]]:
                        return False
                    if out_ord[primitive[nodes[i]]["out"]] == out_ord[primitive[nodes[j]]["out"]]:
                        if nodes[i] > nodes[j]:
                            return False
        return True

    def fill_dag(self, cur, nodes, reps):
        if cur == self.n:
            if self.check_isomorphism(nodes):
                self.filled.append((nodes, reps))
            return
        for x in primitive:
            in_type = primitive[x]["in"]
            in_num = len(in_type)

            # cannot be continuous
            if x in math_op or x in math_c_op:
                if any([nodes[p] in math_op or nodes[p] in math_c_op for p in self.prev[cur]]):
                    continue

            if "filter" in x:
                if any(["filter" in nodes[p] for p in self.prev[cur]]):
                    continue

            if x == "count" and len(self.prev[cur]) == 1 and nodes[self.prev[cur][0]] == "top_k":
                continue

            if cur == self.n - 1 and primitive[x]["out"] == "column":
                continue

            # Start point
            if not self.prev[cur]:
                if x not in math_op:
                    self.fill_dag(cur + 1, nodes + [x], reps + [[-1] * in_num])
            else:
                # Check if prev can fill
                accept = True
                rep_idx = [-1] * in_num
                for p in self.prev[cur]:
                    prev_out_type = primitive[nodes[p]]["out"]
                    for i in range(in_num):
                        if in_type[i] == prev_out_type and rep_idx[i] == -1:
                            rep_idx[i] = p
                            break
                    else:
                        accept = False
                        break
                if not accept:
                    continue

                # Check if cur is filled enough
                if all([r == -1 for r in rep_idx]):
                    continue

                # Check isomorphism for 2 prev of a math_op node
                if x in math_op:
                    if len(self.prev[cur]) == 2:
                        i, j = self.prev[cur][0], self.prev[cur][1]
                        if self.prev[i] == self.prev[j] and self.succ[i] == self.succ[j]:
                            if nodes[i] == "count" and nodes[j] == "count":
                                continue

                self.fill_dag(cur + 1, nodes + [x], reps + [rep_idx])