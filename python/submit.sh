#!/usr/bin/bash
#SBATCH --job-name=TMSIS_python_example
#SBATCH --time=00:20:00
#SBATCH --mail-type=all
#SBATCH --partition=day
#SBATCH --mem=40GB
#SBATCH --cpus-per-task=5
#SBATCH --output=out.txt
#SBATCH -e err.txt

module load Python/3.10.8-GCCcore-12.2.0

# load the virtual environment used for this project
source venv/bin/activate

python example.py


