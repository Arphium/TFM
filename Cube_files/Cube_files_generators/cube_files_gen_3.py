"""
Program to run subsequent FHI-AIMS calculations changing the electric field.
Sends a calculation, waits for the optimized geometry and uses it for the next one.
"""

import os
import shutil
import sys
import time
import subprocess

alpha_carbons_up = [32,59]
alpha_carbons_down = []
constrain_carbons = [8,9] #REMEMBER ONLY THE CARBONS THAT DEFINE THE PLANE

def send_command(command:str):
    """Calls subprocess to send a command to CLI and get the output."""
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)      # Runs the command
    output = process.communicate()[0]                                           # Gets the output of the comand (tail + grep)
    output = output.decode()                                                    # Decodes b\ string

    return output


def copy_files(i:int,tautomer:str):
    """Copy files to the next folder, and to the selected tautomer."""
    if i+1 > 40: print("Sacabó!"); sys.exit()           # Case of the last folder
    origin = f"E_field_{i}/{tautomer}"                 # Current folder
    final = f"E_field_{i}/{tautomer}/superficie"                # Next folder
    #shutil.copy(origin+"control.in",final)              # Copy control.in
    #shutil.copy(origin+"running_bis.sub",final)                 # Copy script
    os.system(f"grep atom {origin+'geometry.in.next_step'} >> {final+'geometry.in'}")   # Copy atom coordinated of optimized geometry
    add_moments(f"{final+'geometry.in'}",spin_up= alpha_carbons_up , spin_down=alpha_carbons_down ,constrain=constrain_carbons)
    os.system(f"echo 'homogeneous_field  0  {0.1*(i+2)}  0' >> {final+'geometry.in'}")   # Add line for new electric field

    ###! Añadir initial moments en atomos concretos de final+geomstry.in !!!


def tail_list(tails:list,tail_output:str):
    """Checks if program is stuck or non converged by comparing 3 consecutive tails."""
    equal = tails[0] == tails[1] == tail_output

    if equal:   # Something went wrong
        print(f"ERROR in folder: {folder}")
        return True
    else:       # Reorder tails list and continue
        tails[0], tails[1] = tails[1], tail_output
        return False


def add_moments(filename,spin_up,spin_down,constrain):
    # Collect info from geometry.in
    no_moment_file = open(filename,'r').readlines()
    save_line = ['atom','constrain_relaxation','homogeneous_field']
    geometry = []
    for line in no_moment_file:
        if line.strip().split()[0] in save_line:
            geometry.append(line)

    # Collect initial_moment to collected info from geometry.in
    moment_file = open(filename,'w')
    count_atoms = 0
    for i,line in enumerate(geometry):
        moment_file.write(line)
        if line.split()[0] == "atom":
            #moment_file.write('constrain_relaxation  x \n')
            count_atoms += 1
            if count_atoms in constrain:
                moment_file.write('constrain_relaxation  x\n')
            if count_atoms in spin_up:
                moment_file.write("initial_moment 1 \n")
            if count_atoms in spin_down:
                moment_file.write("initial_moment -1 \n")

    moment_file.close()

    
###################### MAIN PROGRAM ##################

tautomer = "ENOL_KETO"
#tautomer = "KETO_ENOL"

for i in range(0,100+1):

    folder = f"E_field_{i}/{tautomer}/"            # Folder of the current calculation
    control = f"control_rep/"
    #os.makedirs(f"E_field_{i}/{tautomer}/superficie")     # Make next folder if not present
   

    try: os.makedirs(f"E_field_{i}/{tautomer}/superficie")     # Make next folder if not present
    except FileExistsError: pass
    dire = f"E_field_{i}/{tautomer}/superficie/"
    shutil.copy(control+"control.in",dire) 
    shutil.copy(control+"running_bis.sub",dire)
    os.chdir(folder)  
    # copy_files(i,tautomer)                              # Changes directory to current folder
    if   os.path.exists("fhi-aims.out") :

            #origin = f"E_field_{i}/{tautomer}"                 # Current folder
            final = f"superficie/"                # Next folder
            shutil.copy("geometry.in.next_step",final+"geometry.in.next_step")
            os.chdir(final)  
            os.system(f"grep atom 'geometry.in.next_step' >> 'geometry.in'")
            add_moments(f"geometry.in",spin_up= alpha_carbons_up , spin_down=alpha_carbons_down ,constrain=constrain_carbons)
              # Copy control.in
    #        #shutil.copy(origin+"running_bis.sub",final)
    #        os.system(f"grep atom {origin+'geometry.in.next_step'} >> {final+'geometry.in'}")   # Copy atom coordinated of optimized geometry
    #        add_moments(f"{final+'geometry.in'}",spin_up= alpha_carbons_up , spin_down=alpha_carbons_down ,constrain=constrain_carbons)
    #        os.system(f"echo 'homogeneous_field  0  {0.1*(i+2)}  0' >> {final+'geometry.in'}")   # Add line for new electric field
    #        os.chdir(final)
            os.system(f"qsub running_bis.sub")
    # else :
    #     os.system(f"qsub running_bis.sub")       # Submits calculation using script (os.system() is similar to CLI arguments)

    tails = ["abcdef4" for _ in range(2)]                  # List where the 3 last tails will go (resets for every folder)

    finish_command = "tail fhi-aims.out|grep 'Have a nice day.'"    # Command to see if the calculation has finished correctly
    tail_command = "tail fhi-aims.out"                              # Command to save tail progress (to later handle error cases)
    while True:
        if not os.path.exists("fhi-aims.out"): time.sleep(10); continue             # Wait until the output file exists

        # Checking if the program has finished correctly
        output = send_command(finish_command)
        print(output)
        if "Have a nice day." in output: print("mu bien"); break
        
        # Checking if there is any error (non-convergence, stuck, etc)
        tail_output = send_command(tail_command)
        error = tail_list(tails,tail_output)
        if error: sys.exit()        #! O mejor break?
        
        time.sleep(30)                                                             # else, wait 5 mins

    os.chdir("../../")# Go back to initial directory
    os.chdir("..")
    try: os.makedirs(f"E_field_{i+1}/{tautomer}/")     # Make next folder if not present
    except FileExistsError: pass

    #copy_files(i,tautomer)                          # Copy files to next folder and change E_field



# THINGS TO IMPROVE:
# Lo de initial moments
# Make the E_fielf_{i} folders itself (not external)
# Use argparse and make it CLI friendly (with flags of -min, -max, -tautomer, -time_between, ...)
