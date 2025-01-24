from base_graph import base_graph
from filled_graph import filled_graph
from sample_generate import reasoning_sample
from pickle import dump
from random import seed
import os
from dataset_utils import text_generate, sample_from_candi
from config import config
from primitives import math_op
import json

seed(0)

demo_n, test_n, shot = config.demo_n, config.test_n, config.shot
show_primitive = config.show_primitive

prevs_set = {
4: [
    {0: [ ], 1: [0], 2: [1], 3: [2]},
    {0: [ ], 1: [ ], 2: [0, 1], 3: [2]},
    {0: [], 1: [0], 2: [ ], 3: [1, 2]},
    {0: [ ], 1: [0], 2: [0, 1], 3:[2]},
    {0: [ ], 1: [0], 2: [0], 3: [1, 2]},
    {0: [ ], 1: [0], 2: [1], 3: [1, 2]},
],
3: [
    {0: [ ], 1: [0], 2: [1]},
    {0: [ ], 1: [ ], 2: [0, 1]},
    {0: [ ], 1: [0], 2: [0, 1]}
],
2: [{0: [ ], 1: [0]}],
1: [{0: [ ]}],
}

def get_base(n):
    prevs = prevs_set[n]
    base_store = [ ]
    for i in range(len(prevs)):
        graph = base_graph(prevs[i], i)
        graph.fill_dag(0, [ ], [ ])
        base_store += [filled_graph(graph, nodes, reps) for nodes, reps in graph.filled]
    return base_store


test_base = get_base(test_n)
test_samples = [reasoning_sample(x) for x in test_base]
if demo_n == test_n:
    demo_samples = test_samples
    assert demo_samples[0] == test_samples[0]
else:
    demo_base = get_base(demo_n)
    demo_samples = [reasoning_sample(x) for x in demo_base]

prim_base = get_base(1)
prim_samples = [reasoning_sample(x) for x in prim_base]
prim_samples = {x.graph.nodes[0]: x for x in prim_samples}

prim_2_base = get_base(2)
prim_2_samples = [reasoning_sample(x) for x in prim_2_base]
for x in prim_2_samples:
    for y in x.graph.nodes:
        if y not in prim_samples:
            prim_samples[y] = x

dataset = [ ]

for sample in test_samples:
    if sample.nodes[-1] in math_op:
        continue
    sample_nodes = set(sample.nodes)
    # candi = [x for x in demo_samples if x != sample]
    candi = [x for x in demo_samples if x != sample and any([y in sample_nodes for y in x.nodes])]

    demo = sample_from_candi(candi, shot, sample_nodes, None)

    if show_primitive:
        nodes = sorted(list(set(sample.graph.nodes)))
        for x in nodes:
            assert x in prim_samples
            demo.append(prim_samples[x])

    text = text_generate(demo, sample)

    dataset.append({"input_text": text, "sample": sample, "demo": demo})


if config.complete_sys_gap:
    for i in range(len(dataset)):
        sample, demo = dataset[i]["sample"], dataset[i]["demo"]
        if any([x.graph.graph_tp == sample.graph.graph_tp for x in demo]):
            sample_nodes = set(sample.nodes)
            candi = [x for x in demo_samples if x != sample and any([y in sample_nodes for y in x.nodes])]
            candi = [x for x in candi if x.graph.graph_tp != sample.graph.graph_tp]
            aim_tp = None
            demo = sample_from_candi(candi, shot, sample_nodes, aim_tp)
            if show_primitive:
                nodes = sorted(list(set(sample.graph.nodes)))
                for x in nodes:
                    assert x in prim_samples
                    demo.append(prim_samples[x])
            text = text_generate(demo, sample)
            dataset[i] = {"input_text": text, "sample": sample, "demo": demo}


if config.no_sys_gap:
    for i in range(len(dataset)):
        sample, demo = dataset[i]["sample"], dataset[i]["demo"]
        if not any([x.graph.graph_tp == sample.graph.graph_tp for x in demo]):
            sample_nodes = set(sample.nodes)
            candi = [x for x in demo_samples if x != sample and any([y in sample_nodes for y in x.nodes])]
            aim_tp = sample.graph.graph_tp
            demo = sample_from_candi(candi, shot, sample_nodes, aim_tp)
            if show_primitive:
                nodes = sorted(list(set(sample.graph.nodes)))
                for x in nodes:
                    assert x in prim_samples
                    demo.append(prim_samples[x])
            text = text_generate(demo, sample)
            dataset[i] = {"input_text": text, "sample": sample, "demo": demo}


root = "../dataset"
if not os.path.exists(root):
    os.makedirs(root)

print(config.name)
dump(dataset, open(f"{root}/{config.name}.pkl", "wb"))
f = open(f"{root}/{config.name}.jsonl", "w")
for x in dataset:
    sample, demo = x["sample"], x["demo"]
    y = {"input": sample.question, "output": sample.output_steps,
         "demonstration": [{"input": z.question, "output": z.output_steps} for z in demo]}
    f.write(json.dumps(y) + "\n")
