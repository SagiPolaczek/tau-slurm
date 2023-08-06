import subprocess
from pathlib import Path
from typing import Optional, Union
from tau_slurm.utils import write_shebang, append_to_file, cd


def submit_job(
    command_to_run: Union[str, list[str]],
    workspace_dir: str,  # TODO: rename to workspace_dir_path
    job_name: str,
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

    See https://www.cs.tau.ac.il/system/slurm
    """
    workspace_dir_path = Path(workspace_dir)
    job_dir_path = workspace_dir_path.joinpath(job_name)
    path_to_slurm_file = job_dir_path.joinpath("job.slurm")

    if not output:
        output = job_dir_path.joinpath("o.out").resolve()
    job_dir_path.mkdir(parents=True, exist_ok=True)

    write_shebang(path_to_slurm_file)
    append_to_file(path_to_slurm_file, f"#SBATCH --account={account}")
    append_to_file(path_to_slurm_file, f"#SBATCH --output={output}")
    append_to_file(path_to_slurm_file, f"#SBATCH --partition={partition}")
    append_to_file(path_to_slurm_file, f"#SBATCH --signal={signal}")
    append_to_file(path_to_slurm_file, f"#SBATCH --nodes={nodes}")
    append_to_file(path_to_slurm_file, f"#SBATCH --mem={mem}")
    append_to_file(path_to_slurm_file, f"#SBATCH --cpus-per-task={cpus_per_task}")
    append_to_file(path_to_slurm_file, f"#SBATCH --gpus={gpus}")

    if error:
        append_to_file(path_to_slurm_file, f"#SBATCH --error={error}")

    if time:
        append_to_file(path_to_slurm_file, f"#SBATCH --time={time}")

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
    print(f"Job submitted successfully with output file path: {output}")
