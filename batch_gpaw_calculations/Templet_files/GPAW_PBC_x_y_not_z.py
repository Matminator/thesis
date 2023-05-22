#SBATCH --job-name=AL_JOB_NAME
#SBATCH --mail-type=FAIL  # The default value is the submitting user.
#SBATCH --partition=xeon56
#SBATCH -N 1      # Minimum of 2 nodes
#SBATCH -n 56     # 24 MPI processes per node, 48 tasks in total, appropriate for xeon24 nodes
#SBATCH --time=20:10:00

# *** Imports ***************************************
import ase
from ase import Atoms
from ase.io.trajectory import Trajectory
from ase.io import read, write



from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase.md.langevin import Langevin
from ase import units

from gpaw import GPAW, PW

import numpy as np

# *** Trajectory files ***************************
config = --input_trajectory--
out = --output_trajectory--

# *** Calculator **********************************
# Convergence criteria for GPAW calculator (here the forces
# are included along with the standard criteria):
con_criteria =  {'energy': 0.0005,  # eV / electron
                 'density': 1.0e-4,  # electrons / electron
                 'eigenstates': 4.0e-8,  # eV^2 / electron
                 'bands': 'occupied',
                 'forces': 0.01}

calc = GPAW(
        mode= PW(650),
        xc = 'PBE',
        kpts={'density': 2},
        poissonsolver={'dipolelayer': 'xy'}, # MUST BE CONSIDERED (4)
        convergence = con_criteria,
        symmetry='off'
        )
    
config.set_pbc([True, True, False]) # MUST BE CONSIDERED (3)

config.calc = calc

energy = config.get_potential_energy()
forces = config.get_forces()

out.write(config,forces=forces,energy=energy)
# ******
