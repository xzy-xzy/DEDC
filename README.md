# DEDC
Dataset and code for the paper [Investigating the (De)Composition Capabilities of Large Language Models in Natural-to-Formal Language Conversion](https://arxiv.org/abs/2501.14649).

## Dataset
The dataset is available as `*.jsonl` files in `dataset`. The `*.pkl` files are data files that can be used directly for evaluation codes. For filenames:
- Names with `show_primitive` mean composition only, otherwise they mean decomposition + composition.
- `no_sys_gap` and `complete_sys_gap` refer to the setting of the 0% and 100% composition gap.
- `anom` and `cross` refer to the setting of Anomalous and Cross-mapping for counter-intuitive symbolic names.



## Code
Start by:
```
cd code
```
### Dataset construction
See `construction_complete.sh` for commands to reproduce the data construction.

### Evaluation
Install required packages for LLM API calls with:
```
pip install -r requirements.txt
```
See `eval_complete.sh` for commands for the evaluation.
For models that support the batch API (e.g., GPT-4o), `icl_batch_eval.py` can be used instead of `icl_eval.py` to make batch API calls.

## Citation
```
@misc{xu2025investigatingdecompositioncapabilitieslarge,
      title={Investigating the (De)Composition Capabilities of Large Language Models in Natural-to-Formal Language Conversion}, 
      author={Ziyao Xu and Houfeng Wang},
      year={2025},
      eprint={2501.14649},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2501.14649}, 
}
```
