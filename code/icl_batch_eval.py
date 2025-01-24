from openai import OpenAI
from config import config

import os
from pickle import load
import json

client = OpenAI(api_key=config.api_key)

name = f"{config.model}_{config.name}"

root = f"../{config.name}/{config.model}"

if not os.path.exists(f"../{config.name}"):
    os.mkdir(f"../{config.name}")
if not os.path.exists(root):
    os.mkdir(root)
    
dataset = load(open(f"../dataset/{config.name}.pkl", "rb"))

if not os.path.exists(f"{root}/id.txt"):

    f = open(f"{root}/batch.jsonl", "w")

    for idx, x in enumerate(dataset):
        text = x["input_text"]
        body = {
            "model": config.model,
            "max_tokens": 256,
            "temperature": 0,
            "messages": [
                {"role": "user", "content": text}
            ]
        }
        batch = {
            "custom_id": str(idx),
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": body
        }
        f.write(json.dumps(batch) + "\n")

    f.close( )

    batch_input_file = client.files.create(
      file=open(f"{root}/batch.jsonl", "rb"),
      purpose="batch"
    )

    f = open(f"{root}/id.txt", "w")
    f.write(batch_input_file.id)
    f.close( )

    print("Batch created.")

else:
    print("Batch already created.")


idx = open(f"{root}/id.txt").read( )

if not os.path.exists(f"{root}/bid.txt"):
    ret = client.batches.create(
        input_file_id=idx,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
          "description": f"{name}"
        }
    )
    bid = ret.id
    f = open(f"{root}/bid.txt", "w")
    f.write(bid)
    f.close( )
    print("Batch submitted.")

else:
    bid = open(f"{root}/bid.txt").read( )
    print("Batch already submitted.")

if not os.path.exists(f"{root}/result"):
    ret = client.batches.retrieve(bid)
    if ret.status == "completed":
        os.mkdir(f"{root}/result")
        idx = ret.output_file_id
        response = client.files.content(idx)
        text = response.text
        # f = open(f"{root}/result.txt", "w")
        text = text.split("\n")
        if len(text[-1]) == 0:
            text = text[:-1]
        ret = [ ]
        for line in text:
            t = json.loads(line)
            custom_id = int(t["custom_id"])
            content = t["response"]["body"]["choices"][0]["message"]["content"]
            ret.append((custom_id, content))
        ret.sort(key=lambda x: x[0])
        for idx, content in ret:
            f = open(f"{root}/result/{idx}.txt", "w")
            f.write(content)
            f.close( )
        print("Batch completed.")
    else:
        print("Batch not completed.")
        exit(0)

else:
    print("Batch already completed.")


from sample_generate import convert_to_one

g = open(f"{root}/eval.txt", "w")

tot, rit = 0, 0
for idx, x in enumerate(dataset):
    f = open(f"{root}/result/{idx}.txt")
    pred = f.read( )
    pred = pred.replace("`", "").replace("plaintext", "")
    x, d, t = x["sample"], x["demo"], x["input_text"]
    pred_one = convert_to_one(pred)
    result = any([pred_one == y for y in x.candi_outputs])
    rit += result
    tot += 1
    g.write(f"question: {x.question}\ngold: {x.output_steps}\npred: {pred}\n"
            f"gold_one: {x.candi_outputs[0]}\npred_one: {pred_one}\nresult: {result}\ntype: {x.graph.graph_tp}\n"
            f"demo_type: {[y.graph.graph_tp for y in d]}\n"
            f"train_nodes: {[y.nodes for y in d]}\n"
            f"=====================\n")

print(rit, tot, rit / tot * 100)



