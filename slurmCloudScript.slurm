#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks=1
#SBATCH --output=Crawler.out
#SBATCH --time=0-24:00:00
module load foss/2019b
module load python/3.8

#module load XXXXX/1.1.1          # If want to include python library, find it and copy paster to this
srun python3 Tweepy.py

## DO NOT EDIT BEYOND ###
# Job Monitor command to monitor resource usage
my-job-stats -a -n -s