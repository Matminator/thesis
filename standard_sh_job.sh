#!/bin/bash -le
#SBATCH --mail-type=END,FAIL
#SBATCH --partition=sm3090
#SBATCH -N 1      # Minimum of 1 node
#SBATCH -n 8     # 8 MPI processes per node
#SBATCH --time=08:00:00
#SBATCH --gres=gpu:RTX3090:1

source $HOME/thesis/thesis_venv/bin/activate

nequip-train /home/niflheim/s173973/thesis/AuTiO2_Prototyping/gridSearch/num_layers_Iblocks=8.yaml

nequip-deploy build --train-dir /home/niflheim/s173973/thesis/AuTiO2_Prototyping/gridSearch/num_layers_Iblocks/NequIP-layers=1 NequIP-layers=1.pth

