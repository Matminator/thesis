import numpy as np
import ase
from ase import Atoms
from ase.cluster.cubic import FaceCenteredCubic

def wulff_construction(energies, wanted_atoms, lower_number = True, lattice_constant = 3.9160, element = 'Pt', fac_step = 0.05, print_result = True):
    """
    energies: energies of crystal facets
    wanted_atoms: number of atoms wanted in the constructed Wulff shape.
    lower_number: if True, takes returns the structure with the largest
    amount of atoms below wanted_atoms. If false, returns the smallest above
    wanted_atoms.
    lattice_constant: lattice constant of the bulk FCC crystal.
    Element: chemical element.
    print_result: print the resulting number of atoms and respective layers.
    """
    
    # The surfaces of this Wulff construction:
    surfaces = ((1,0,0),(1,1,0),(1,1,1),(-1,-1,-1))
    
    # Computing lengths of lattice directions based on lattice constant:
    l_100 = np.sqrt(1) * lattice_constant / 2
    l_110 = np.sqrt(2) * lattice_constant / 4
    l_111 = np.sqrt(3) * lattice_constant / 3
    L = np.array([l_100, l_110, l_111, l_111])

    EL = energies / L
    
    fac = 0
    n_atoms = 0
    while n_atoms < wanted_atoms:
        fac += fac_step
        layers = (EL * fac).astype(int)
        atoms = FaceCenteredCubic(element, surfaces, layers)
        n_atoms = len(atoms)

    if lower_number:
        # Taking the configuration smaller than the wanted number of atoms:
        fac -= fac_step
        layers = (EL * fac).astype(int)
        atoms = FaceCenteredCubic(element, surfaces, layers)
        
    if print_result:
        print('Resulting number of atoms:', len(atoms))
        print('Resulting number of layers:', layers)
        
    # Rotating the atoms object such that (-1,-1,-1) faces -z
    atoms.rotate((1,1,1), (0,0,np.sqrt(3)))  
    
    return atoms
