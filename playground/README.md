# Genrate training set

## SlidesBench examples
1. Initialize base data under `/data`

```bash
python init_data.py
```

2. Generate training data

```bash
gpu "python generate_dataset.py --data_dir ./data --model gpt-4o"
gpu --large-mem "python generate_dataset.py --data_dir ./data --model llava-ov --test 1"
```
## Visualization
```bash
cd .. # under repo root dir
streamlit run training_data_dashboard.py
```