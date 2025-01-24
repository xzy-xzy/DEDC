def convert(x):
    if x == "row":
        return "view"
    if x == "column":
        return "value"
    return x


def question_generate(graph, f_nodes):
    n = graph.n
    idx, tp = graph.idx, graph.tp[:n - 1]
    nodes = graph.nodes
    tp = tuple([convert(x) for x in tp])
    q = None

    if n == 1:
        f0 = f_nodes[0]
        if nodes[0] != "hop":
            q = f"{f0.question( )} {f0.link_scope} all items?"
        else:
            q = f"what is {f0.leaf_value( )}?"

    if n == 2:
        f0, f1 = f_nodes[0], f_nodes[1]
        if tp[0] == "view":
            q = f"{f1.question( )} {f1.link_scope} {f0.scope( )}?"
        elif tp[0] == "value":
            q = f"{f1.question(val=f0.leaf_value( ))}?"

    if n == 3:
        f0, f1, f2 = f_nodes[0], f_nodes[1], f_nodes[2]
        if idx == 0:
            if tp == ("view", "view"):
                q = f"Among {f0.leaf_scope( )}, {f2.question( )} {f2.link_scope} {f1.scope( )} among them?"
            elif tp == ("view", "value"):
                v = f"{f1.value( )} {f1.link_scope} {f0.leaf_scope( )}"
                q = f"Among all items, {f2.question(val=v)}?"
            elif tp == ("value", "view"):
                q = f"{f2.link_scope} {f1.scope(val=f0.leaf_value( ))}, {f2.question( )}?"
            elif tp == ("value", "value"):
                v = f"{f1.value(val=f0.leaf_value( ))}"
                q = f"Among all items, {f2.question(val=v)}?"
            else:
                assert False
        elif idx == 1:
            if tp == ("view", "value"):
                q = f"Among {f0.leaf_scope( )}, {f2.question(val=f1.leaf_value( ))}?"
            elif tp == ("value", "value"):
                q = f"Among all items, {f2.question(val=f0.leaf_value( ), val2=f1.leaf_value( ))}?"
            else:
                assert False
        elif idx == 2:
            if tp == ("view", "value"):
                v = f"{f1.value( )} {f1.link_scope} them"
                q = f"Among {f0.leaf_scope( )}, {f2.question(val=v)}?"
            else:
                assert False
        else:
            assert False

    if n == 4:
        f0, f1, f2, f3 = f_nodes[0], f_nodes[1], f_nodes[2], f_nodes[3]
        if idx == 0:
            if tp == ("view", "view", "view"):
                q = f"Among {f1.scope( )} {f1.link_scope} {f0.leaf_scope( )}, " \
                    f"{f3.question( )} {f3.link_scope} {f2.scope( )} among them?"
            elif tp == ("view", "view", "value"):
                v = f"{f2.value( )} {f2.link_scope} {f1.scope( )} {f1.link_scope} {f0.leaf_scope( )}"
                q = f"Among all items, {f3.question(val=v)}?"
            elif tp == ("view", "value", "view"):
                v = f"{f1.value( )} {f1.link_scope} {f0.leaf_scope( )}"
                q = f"{f3.link_scope} {f2.scope(val=v)}, {f3.question( )}?"
            elif tp == ("view", "value", "value"):
                v1 = f"{f1.value( )} {f1.link_scope} {f0.leaf_scope( )}"
                v2 = f"{f2.value(val=v1)}"
                q = f"Among all items, {f3.question(val=v2)}?"
            elif tp == ("value", "view", "view"):
                q = f"Among {f1.scope(val=f0.leaf_value( ))}, " \
                    f"{f3.question( )} {f3.link_scope} {f2.scope( )} among them?"
            elif tp == ("value", "view", "value"):
                v = f"{f2.value( )} {f2.link_scope} {f1.scope(val=f0.leaf_value( ))}"
                q = f"Among all items, {f3.question(val=v)}?"
            elif tp == ("value", "value", "view"):
                v = f"{f1.value(val=f0.leaf_value( ))}"
                q = f"{f3.link_scope} {f2.scope(val=v)}, {f3.question( )}?"
            elif tp == ("value", "value", "value"):
                q = f"Among all items, {f3.question(val=f2.value(val=f1.value(val=f0.leaf_value( ))))}?"
            else:
                assert False
        elif idx == 1:
            if tp == ("view", "value", "view"):
                q = f"Among {f0.leaf_scope( )}, " \
                    f"{f3.question( )} {f3.link_scope} {f2.scope(val=f1.leaf_value( ))}?"
            elif tp == ("value", "value", "value"):
                q = f"Among all items, {f3.question(val=f2.value(val=f0.leaf_value( ), val2=f1.leaf_value( )))}?"
            else:
                assert False
        elif idx == 2:
            if tp == ("view", "view", "value"):
                q = f"Among {f1.scope( )} {f1.link_scope} {f0.leaf_scope( )}, " \
                    f"{f3.question(val=f2.leaf_value( ))}?"
            elif tp == ("view", "value", "view"):
                v = f"{f1.value( )} {f1.link_scope} {f0.leaf_scope( )}"
                q = f"Among {f2.leaf_scope( )}, {f3.question(val=v)}?"
            elif tp == ("view", "value", "value"):
                v = f"{f1.value( )} {f1.link_scope} {f0.leaf_scope( )}"
                q = f"{f3.question(val=v, val2=f2.leaf_value( ))}?"
            elif tp == ("value", "value", "view"):
                v = f"{f1.value(val=f0.leaf_value( ))}"
                q = f"Among {f2.leaf_scope()}, {f3.question(val=v)}?"
            else:
                assert False
        elif idx == 3:
            if tp == ("view", "value", "view"):
                v = f"{f1.value( )} {f1.link_scope} them"
                q = f"Among {f0.leaf_scope( )}, " \
                    f"{f3.question( )} {f3.link_scope} {f2.scope(val=v)} among them?"
            else:
                assert False
        elif idx == 4:
            if tp == ("view", "view", "value"):
                v = f"{f2.value( )} {f2.link_scope} group A"
                q = f"Assuming that group A contains {f0.leaf_scope( )}, " \
                    f"{f3.question(val=v)} {f3.link_scope} {f1.scope( )} among group A?"
            elif tp == ("view", "value", "value"):
                v1 = f"{f1.value( )} {f1.link_scope} them"
                v2 = f"{f2.value( )} {f2.link_scope} them"
                q = f"Among {f0.leaf_scope( )}, " \
                    f"{f3.question(val=v1, val2=v2)}?"
            else:
                assert False
        elif idx == 5:
            if tp == ("view", "view", "value"):
                v = f"{f2.value( )} {f2.link_scope} them"
                q = f"Among {f1.scope( )} {f1.link_scope} {f0.leaf_scope( )}, " \
                    f"{f3.question(val=v)}?"
            else:
                assert False
    assert q is not None
    q = q[0].upper( ) + q[1:]
    return q








