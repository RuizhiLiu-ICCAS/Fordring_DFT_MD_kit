#AIMDkit
#Created by Rui-Zhi Liu_ICCAS
#Version 1.0 
#2025.2.21
#此程序和 OSZICAR; XDATCAR; XDATCAR_toolkit.py 需要在同一文件夹
#目前此程序仅具有统计分子动力学模拟能量收敛及批处理不同帧数RDF的功能

import argparse
import os
import numpy as np
import subprocess
import MDAnalysis
import MDAnalysis.analysis.rdf

def call_xdatcar_toolkit(end):
    return_code = subprocess.call(['python', 'XDATCAR_toolkit.py', '-p' , '-e', str(end), '-t', '1', '--pbc'])
    if return_code != 0:
        raise RuntimeError('XDATCAR_toolkit.py returned non-zero exit status')
    return return_code

def run_rdf_calculation(atom1, atom2, step, end_frame):
    start_frame = 1
    print("Tips: The Start frame is 1, and it cannot change.")
    for i in range(start_frame + step, end_frame + step, step):
        print(f"Running for start frame {start_frame} to end frame {i}")
        call_xdatcar_toolkit(i)

        u = MDAnalysis.Universe('XDATCAR.pdb', permissive=True)
        g1 = u.select_atoms(f'type {atom1}')
        g2 = u.select_atoms(f'type {atom2}')
        rdf = MDAnalysis.analysis.rdf.InterRDF(g1,g2,nbins=75, range=(0.0, min(u.dimensions[:3])/2.0))

        rdf.run()

        directory = f"{g1.atoms.types[0]}-{g2.atoms.types[0]}"
        os.makedirs(directory, exist_ok=True)

        np.savetxt(os.path.join(directory, f'{i}.txt'), np.column_stack((rdf.bins, rdf.rdf)), fmt='%1.6f')

def run_energy_calculation():
    os.system("grep E0 OSZICAR > E0.txt")

    filename = 'E0.txt'

    with open(filename, 'r') as f:
        lines = f.readlines()

    totalE = []

    for line in lines:
        idxE0 = line.find('E0=')
        idxEK = line.find('EK=')

        if idxE0 == -1 or idxEK == -1:
            continue

        E0 = float(line[idxE0+3:].split()[0])
        EK = float(line[idxEK+3:].split()[0])

        totalE.append(E0 + EK)

    with open('totalE.txt', 'w') as f:
        for item in totalE:
            f.write("%s\n" % item)
    
    if os.path.exists('E0.txt'):
        os.remove('E0.txt')
    else:
        print("The file E0.txt does not exist")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='This script provides different methods for molecular dynamics simulations analysis.', formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('-Energycal', action='store_true', help='''Run energy calculation. Extracts energy data from OSZICAR file and writes the results into totalE.txt.
python AIMD.py -Energycal
-----------------------''')

    parser.add_argument('-RDF', action='store_true', help='''Run RDF calculation.
For the RDF calculation you have to define additional parameters (see below):
python AIMDkit.py -RDF -atom1 Al -atom2 S -step 100 -end_frame 5000
-----------------------''')

    parser.add_argument('-atom1', type=str, help='Type of atom 1 for RDF calculation. For example: -atom1 Al')
    parser.add_argument('-atom2', type=str, help='Type of atom 2 for RDF calculation. For example: -atom2 S')
    parser.add_argument('-step', type=int, help='Step for RDF calculation. Defines the step size for frames in the simulation. For example: -step 100')
    parser.add_argument('-end_frame', type=int, help='End frame for RDF calculation. Defines the last frame for RDF calculation. For example: -end_frame 5000')

    args = parser.parse_args()

    if args.RDF:
        run_rdf_calculation(args.atom1, args.atom2, args.step, args.end_frame)
    elif args.Energycal:
        run_energy_calculation()
    else:
        print("Please provide a valid argument. Run 'AIMDkit.py -h' for more information.")
