import os
import subprocess
from typing import Optional, Union
from tau_slurm.utils import create_directory, write_shebang, append_to_file, cd


def submit_job(
    command_to_run: Union[str, list[str]],
    workspace_dir: str,
    job_name: str,
    context_dir: Optional[str] = None,
    load_bashrc: bool = False,
    account: str = "gpu-research",
    output: Optional[str] = None,
    error: Optional[str] = None,
    partition: str = "gpu-a100-killable",
    time: Optional[int] = None,
    signal: str = "USR1@120",
    nodes: int = 1,
    mem: int = 50000,
    cpus_per_task: int = 4,
    gpus: int = 1,
    constraint: Optional[str] = None,
) -> None:
    """Wrapper to submit a job on the Uni's cluster

    Parameters:
    command_to_run (str):
    workspace_dir (str):
    job_name (str):
    context_dir optional(str):
    load_bashrc (bool):
    """
    job_dir = os.path.join(workspace_dir, job_name)
    path_to_slurm_file = os.path.join(job_dir, "job.slurm")

    if not output:
        output = os.path.join(job_dir, "job.out")
    output = os.path.abspath(output)

    create_directory(workspace_dir)
    create_directory(job_dir)

    write_shebang(path_to_slurm_file)

    append_to_file(path_to_slurm_file, f"#SBATCH --account={account}")
    append_to_file(path_to_slurm_file, f"#SBATCH --output={output}")

    if error:
        append_to_file(path_to_slurm_file, f"#SBATCH --error={error}")

    append_to_file(path_to_slurm_file, f"#SBATCH --partition={partition}")

    if time:
        append_to_file(path_to_slurm_file, f"#SBATCH --time={time}")

    append_to_file(path_to_slurm_file, f"#SBATCH --signal={signal}")
    append_to_file(path_to_slurm_file, f"#SBATCH --nodes={nodes}")
    append_to_file(path_to_slurm_file, f"#SBATCH --mem={mem}")
    append_to_file(path_to_slurm_file, f"#SBATCH --cpus-per-task={cpus_per_task}")
    append_to_file(path_to_slurm_file, f"#SBATCH --gpus={gpus}")

    if constraint:
        append_to_file(path_to_slurm_file, f"#SBATCH --constraint={constraint}")

    if load_bashrc:
        append_to_file(path_to_slurm_file, "source ~/.bashrc")

    if not isinstance(command_to_run, list):
        command_to_run = [command_to_run]

    for command in command_to_run:
        append_to_file(path_to_slurm_file, command)

    if context_dir:
        with cd(context_dir):
            subprocess.run(f"sbatch {path_to_slurm_file}", shell=True, check=True)
    else:
        subprocess.run(f"sbatch {path_to_slurm_file}", shell=True, check=True)
    print(f"Job submitted successfully. Output file path: {output}")
