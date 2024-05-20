#!/bin/sh

#SBATCH --job-name="evaluate_honours"
#SBATCH --partition=gpu
#SBATCH --account=education-eemcs-courses-cse3000
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-task=1
#SBATCH --mem=10GB

# Note that, in an educational account, we cannot use more than 64 CPUs, 2 GPUs,
# and 185GB of memory, and a job cannot run longer than 24 hours


module load 2023r1
module load openmpi
module load python
module load py-numpy
module load py-matplotlib
module load py-pip

pip install optuna
pip install pandas

srun evaluation/evaluation.py > output.log