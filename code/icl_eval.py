from openai import OpenAI
from config import config
from anthropic import Anthropic
from mistralai import Mistral
from time import sleep

if "claude" in config.model:
    client = Anthropic(api_key=config.api_key)
elif "mistral" in config.model:
    client = Mistral(api_key=config.api_key)
else:
    client = OpenAI(api_key=config.api_key, base_url=config.base_url)


def get_response(text):
    try:
        if "claude" in config.model:
            response = client.messages.create(
                model=config.model,
                messages=[{"role": "user", "content": [{"type": "text", "text": text}]}],
                max_tokens=256,
                temperature=0,
                stream=False
            )
            return response.content[0].text
        elif "mistral" in config.model:
            response = client.chat.complete(
                model=config.model,
                messages=[{"role": "user", "content": text}],
                max_tokens=256,
                temperature=0,
                stream=False
            )
            return response.choices[0].message.content
        else:
            response = client.chat.completions.create(
                model=config.model,
                messages=[{"role": "user", "content": text}],
                max_tokens=256,
                temperature=0,
                stream=False
            )
            return response.choices[0].message.content
    except Exception as e:
        print(e)
        return None


import os
from tqdm import tqdm
from pickle import load

root = f"../{config.name}/{config.model}"

if not os.path.exists(f"../{config.name}"):
    os.mkdir(f"../{config.name}")
if not os.path.exists(root):
    os.mkdir(root)

dataset = load(open(f"../dataset/{config.name}.pkl", "rb"))

i = -1

for x in tqdm(dataset):
    i += 1
    if os.path.exists(f"{root}/{i}.txt"):
        continue
    text = x["input_text"]
    output = get_response(text)
    if output is None:
        continue
    o = open(f"{root}/{i}.txt", "w")
    o.write(output)
    o.close( )
    sleep(1.5)

from sample_generate import convert_to_one

f = open(f"{root}/result.txt", "w")

tot, rit = 0, 0
for i, x in enumerate(dataset):
    x, d, t = x["sample"], x["demo"], x["input_text"]
    pred = open(f"{root}/{i}.txt").read( )
    pred_one = convert_to_one(pred)
    result = any([pred_one == y for y in x.candi_outputs])
    rit += result
    tot += 1
    f.write(f"question: {x.question}\ngold: {x.output_steps}\npred: {pred}\n"
            f"gold_one: {x.candi_outputs[0]}\npred_one: {pred_one}\nresult: {result}\ntype: {x.graph.graph_tp}\n"
            f"demo_type: {[y.graph.graph_tp for y in d]}\n"
            f"train_nodes: {[y.nodes for y in d]}\n"
            "=====================\n")

print(rit, tot, rit / tot * 100)