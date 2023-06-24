# tau-slurm
TAU's SLURM utils
## Installation
```
pip install -e .
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

Where the hydra config located at `./configs/gen_demo` and looks like:
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


## Useful linux commands

#### Check memory disk space usage and sort it:
```
du -h . | sort -h
```
