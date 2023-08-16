# 🛠️ TAU's SLURM utils 🛠️
## Installation
```
git clone https://github.com/SagiPolaczek/tau-slurm.git
cd tau-slurm
pip install -e .
# If you intend to contribute consider to install with:
pip install -e .[dev]
```

## Usage Examples

### Command Line
##### Minimal args (NOTE: will use default args)
```
$ python ./tau_slurm/submit.py 'bash run_gcg_individual.sh llama2 behaviors'
Submitted batch job 10162
🚀 Job submitted successfully with output file path @ <MY_HOME_DE_FACTO>/tau_slurm_workspace/tau-slurm_j_2023-08-16_10:08:37/o.out
```
##### With kwargs
```
$ python ./tau_slurm/submit.py 'bash run_gcg_individual.sh llama2 behaviors' --job_name example --workspace_dirpath <MY_HOME_DE_FACTO>/sandbox
Submitted batch job 10163
🚀 Job submitted successfully with output file path @ <MY_HOME_DE_FACTO>/sandbox/example/o.out
```

### With a json config file
See [jsonargparse docs](https://jsonargparse.readthedocs.io/en/stable/#configuration-files)
### Hydra Config

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

Where the hydra config path is `./configs/gen_demo.yaml` and looks like*:
```yaml
script_path: ${oc.env:MY_GIT_REPOS}/lit-llama/generate.py
checkpoint_path: ${oc.env:MY_GIT_REPOS}/lit-llama/checkpoints/lit-llama/7B/lit-llama.pth
prompt: "Hello, my name is"
now_date_and_time: ${now:%Y-%m-%d}_${now:%H-%M-%S}

job_kwargs:
  command_to_run: "python ${script_path} --prompt '${prompt}' --checkpoint_path '${checkpoint_path}'"
  workspace_dirpath: ${oc.env:MY_SANDBOX}
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
1. If `error` is not specified is your SLURM config, the output file will contain both the stdout and stderr streams in a well-organized manner.
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

# Added git-lfs to paths (consider the path)
# See: https://stackoverflow.com/a/73244433 ,
export PATH=$PATH:$HOME_DE_FACTO/packages/git-lfs-3.2.0/

# Activate the most used conda env
conda activate env_name
```
