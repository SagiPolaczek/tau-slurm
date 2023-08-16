import os
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Union
from jsonargparse import CLI
from tau_slurm.utils import write_shebang, append_to_file, cd

def submit_job(
    command_to_run: Union[str, list[str]],
    *,
    job_name: Optional[str],
    workspace_dirpath: Optional[Union[str,Path]] = None,
    context_dir: Optional[str] = None,
    load_bashrc: bool = False,
    account: str = "gpu-research",
    output: Optional[Path] = None,
    error: Optional[Path] = None,
    partition: str = "gpu-a100-killable",
    time: Optional[int] = None,
    signal: str = "USR1@120",
    nodes: int = 1,
    mem: int = 50000,
    cpus_per_task: int = 4,
    gpus: int = 1,
    constraint: Optional[str] = None,
) -> None:
    """
    Wrapper to submit a job on the Uni's cluster
    
    See README & https://www.cs.tau.ac.il/system/slurm
    """
    if workspace_dirpath is None:
        if "HOME_DE_FACTO" not in os.environ:
            raise Exception(f"You should either supply a 'workspace_dirpath' or define an env varible 'HOME_DE_FACTO' which will point to your home directory with your research/project/course group.")
        workspace_dirpath = Path(os.environ["HOME_DE_FACTO"]).joinpath("tau_slurm_workspace")
    else:
        workspace_dirpath = Path(workspace_dirpath)

    if job_name is None:
        current_date_time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        job_name = f"tau-slurm_j_{current_date_time}"
    job_dirpath = workspace_dirpath.joinpath(job_name)
    slurm_filepath = job_dirpath.joinpath("job.slurm")

    if not output:
        output = job_dirpath.joinpath("o.out").resolve()
    job_dirpath.mkdir(parents=True, exist_ok=True)

    write_shebang(slurm_filepath)
    append_to_file(slurm_filepath, f"#SBATCH --account={account}")
    append_to_file(slurm_filepath, f"#SBATCH --output={output}")
    append_to_file(slurm_filepath, f"#SBATCH --partition={partition}")
    append_to_file(slurm_filepath, f"#SBATCH --signal={signal}")
    append_to_file(slurm_filepath, f"#SBATCH --nodes={nodes}")
    append_to_file(slurm_filepath, f"#SBATCH --mem={mem}")
    append_to_file(slurm_filepath, f"#SBATCH --cpus-per-task={cpus_per_task}")
    append_to_file(slurm_filepath, f"#SBATCH --gpus={gpus}")

    if error:
        append_to_file(slurm_filepath, f"#SBATCH --error={error}")

    if time:
        append_to_file(slurm_filepath, f"#SBATCH --time={time}")

    if constraint:
        append_to_file(slurm_filepath, f"#SBATCH --constraint={constraint}")

    if load_bashrc:
        append_to_file(slurm_filepath, "source ~/.bashrc")

    if not isinstance(command_to_run, list):
        command_to_run = [command_to_run]

    for command in command_to_run:
        append_to_file(slurm_filepath, command)

    if context_dir:
        with cd(context_dir):
            subprocess.run(f"sbatch {slurm_filepath}", shell=True, check=True)
    else:
        subprocess.run(f"sbatch {slurm_filepath}", shell=True, check=True)
    print(f"🚀 Job submitted successfully with output file path @ {output}")

if __name__ == "__main__":
    CLI(submit_job)