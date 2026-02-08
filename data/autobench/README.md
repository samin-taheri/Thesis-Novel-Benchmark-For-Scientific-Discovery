# Auto-Bench (local subset)

Place an Auto-Bench exported subset here.

Expected formats supported by this repository:

## (1) JSONL (recommended)
Each line is a JSON object with fields (best-effort):
- `id` (string)
- `domain` (e.g., physics, biology)
- `nodes` (list[str])
- `edges` (list[list[str,str]] or list["A->B"])
- `prompt` (optional; if missing we will build a prompt from nodes + setting)
- `split` (iid|ood)

Example:
```json
{"id":"ab-1","domain":"physics","nodes":["A","B"],"edges":[["A","B"]],"split":"iid"}
```

## (2) JSON
A single JSON file containing a list of objects with the same fields as above.

If you have the official Auto-Bench format, we can add a dedicated parser once you drop one sample file into this folder.
