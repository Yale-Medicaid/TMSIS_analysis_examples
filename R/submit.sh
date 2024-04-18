#!/usr/bin/bash
#SBATCH --job-name=TMSIS_example_analysis 
#SBATCH --time=00:20:00
#SBATCH --mail-type=all
#SBATCH --partition=day
#SBATCH --mem=40GB
#SBATCH --cpus-per-task=5
#SBATCH --output=out.txt
#SBATCH -e err.txt

module add R/4.3.0-foss-2020b

Rscript example.R


