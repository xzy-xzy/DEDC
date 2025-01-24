from primitives import primitive


def convert(x):
    y = primitive[x]["out"]
    if y == "row":
        return "view"
    if y == "column":
        return "value"
    return y


class filled_graph:
    def __init__(self, base, nodes, reps):
        self.n = base.n
        self.prev = base.prev
        self.succ = base.succ
        self.nodes = nodes
        self.reps = reps
        self.g = (base.idx, tuple(nodes))
        self.idx = base.idx
        self.tp = tuple([primitive[x]["out"] for x in nodes])
        self.key = (self.idx, self.nodes)

        # Get Subgraph
        self.subgraph = [ ]
        skip = set( )
        for i in range(self.n):
            if i in skip:
                continue
            if len(self.prev[i]) == 1:
                self.subgraph.append((0, (nodes[i], nodes[self.prev[i][0]])))
            if len(self.prev[i]) == 2:
                a, b = self.prev[i][0], self.prev[i][1]
                if nodes[a] > nodes[b]:
                    a, b = b, a
                self.subgraph.append((1, (nodes[i], nodes[a], nodes[b])))
            if len(self.succ[i]) == 2:
                a, b = self.succ[i][0], self.succ[i][1]
                tp = 3 if b in self.succ[a] else 2
                if tp == 3 and nodes[a] > nodes[b]:
                    a, b = b, a
                self.subgraph.append((tp, (nodes[i], nodes[a], nodes[b])))
                skip.add(a)
                skip.add(b)

        nodes = [convert(x) for x in nodes]
        self.graph_tp = (self.idx, tuple(nodes[:-1]))
        self.out_tp = list(self.tp)
