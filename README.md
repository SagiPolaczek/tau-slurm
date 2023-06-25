# 🛠️ TAU's SLURM utils 🛠️
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

# .bashrc
### Useful `~/.bashrc` additions
```bash
# The actual home directory (mostly for space reasons)
export HOME_DE_FACTO="<ADD YOUR PATH>"

## CACHE STUFF ##
# Solves 'WARNING: Building wheel for lit failed: [Errno 122] Disk quota exceeded:' when trying to pip install torch.
export PIP_CACHE_DIR="$HOME_DE_FACTO/.cache"
# Redirect HuggingFace cache
export HF_DATASETS_CACHE="$HOME_DE_FACTO/.cache"
export HUGGINGFACE_HUB_CACHE="$HOME_DE_FACTO/.cache"
export HF_HOME="$HOME_DE_FACTO/hugging_face"


## USEFUL ALIASES ##
alias python="python3"
export MY_GIT_REPOS="$HOME_DE_FACTO/git_repos"
export MY_SANDBOX="$HOME_DE_FACTO/sandbox"

# Activate the most used conda env
conda activate env_name
```
