from random import sample


def sample_from_candi(candi, shot, sample_nodes, aim_tp):
    while True:
        demo = sample(candi, shot)
        prim = set( )
        for d in demo:
            for x in d.nodes:
                prim.add(x)
        if all([p in prim for p in sample_nodes]):
            if aim_tp is None or any([d.graph.graph_tp == aim_tp for d in demo]):
                break
    return demo


def text_generate(demo, sample):
    text = "For a given question of tabular reasoning, " \
           "output the reasoning expressions with minimum steps using a particular symbolic system. " \
           "Here are some examples.\n"
    for d in demo:
        text += f"Question: {d.question}\n"
        text += f"Answer: {d.output_steps}\n"

    text += "Now it's your turn. Just output the answer, don't output anything else.\n"
    text += f"Question: {sample.question}\n"
    text += f"Answer:"
    return text
