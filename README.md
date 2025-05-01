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
@inproceedings{xu-wang-2025-investigating,
    title = "Investigating the (De)Composition Capabilities of Large Language Models in Natural-to-Formal Language Conversion",
    author = "Xu, Ziyao  and
      Wang, Houfeng",
    editor = "Chiruzzo, Luis  and
      Ritter, Alan  and
      Wang, Lu",
    booktitle = "Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)",
    month = apr,
    year = "2025",
    address = "Albuquerque, New Mexico",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.naacl-long.87/",
    pages = "1767--1783",
    ISBN = "979-8-89176-189-6",
}
```
