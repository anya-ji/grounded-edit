# Genrate training set

## SlidesBench examples
1. Initialize base data

```bash
python init_data.py
```

2. Generate training data

```bash
gpu "python generate_dataset.py --data_dir ./data --num_iter 10 --model gpt-4o"
```
