# Code for paper 'Beyond Non-Expert Demonstrations: Outcome-Driven Action Con-
straint for Offline Reinforcement Learning'

## 1. Requirements

To install the required dependencies:
  
```bash
conda create -n cum python=3.7
conda activate cum
pip install --no-cache-dir -r requirements.txt
```

## 2. Usage

### 2.1 Training 

```bash
python -m scripts.sac --env_name [ENVIRONMENT] --num_qs 10 --norm_input --load_config_type 'benchmark' --exp_prefix RORL
```

### 2.2 Evaluation

```bash
python -m scripts.sac --env_name [ENVIRONMENT] --num_qs 10 --norm_input --eval_no_training --load_path [model path] --exp_prefix eval_RORL
```


The project is based on YangRui2015's [RORL](https://github.com/YangRui2015/RORL) project.
