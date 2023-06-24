# tau-slurm
## 🛠️ TAU's SLURM utils 🛠️
## Installation
```
git clone https://github.com/SagiPolaczek/tau-slurm.git
cd tau-slurm
pip install -e .
# If you intend to contribute consider to install with:
pip install -e .[dev]
```

## Usage Example

script:
```python
from tau_slurm.submit import submit_job
from omegaconf import DictConfig
import hydra


@hydra.main(config_path="./configs", config_name="gen_demo", version_base="1.2")
def main(cfg: DictConfig):
    submit_job(**cfg["job_kwargs"])

if __name__ == "__main__":
    main()
```

Where the hydra config located at `./configs/gen_demo` and looks like*:
```yaml
script_path: ${oc.env:MY_GIT_REPOS}/lit-llama/generate.py
checkpoint_path: ${oc.env:MY_GIT_REPOS}/lit-llama/checkpoints/lit-llama/7B/lit-llama.pth
prompt: "Hello, my name is"
now_date_and_time: ${now:%Y-%m-%d}_${now:%H-%M-%S}

job_kwargs:
  command_to_run: "python ${script_path} --prompt '${prompt}' --checkpoint_path '${checkpoint_path}'"
  workspace_dir: ${oc.env:MY_SANDBOX}
  job_name: "gen_demo_${now_date_and_time}"
  time: 1
  ```

You can also deploy your job within a context dir:
```yaml
now_date_and_time: ${now:%Y-%m-%d}_${now:%H-%M-%S}

# Paths
script_path: generate.py

# Set prompt
prompt: "Hello, my name is Elon Musk,"
max_new_tokens: 40

job_kwargs:
  command_to_run: "python ${script_path} --prompt '${prompt}'"
  workspace_dir: ${oc.env:MY_SANDBOX}
  job_name: "gen_demo_context_${now_date_and_time}"
  context_dir: ${oc.env:MY_GIT_REPOS}/lit-llama
  time: 10

```


\* Assumes there are env variable `MY_GIT_REPOS` and `MY_SANDBOX`.


# Tips
1. If `error` is not specified, the output file will contain both the stdout and stderr streams in a well-organized manner.
2. Your turn 🫵🏼
