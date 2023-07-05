
"Programm that generates the charge density difference  between two  cube file . Made  by Arnau Cortés Llamas"
"IMPORTANT visualize the cube file and change it to your format "
import os
import shutil
import sys
import time
import subprocess
import numpy as np
import ase 
import ase.io.cube as cube 

tautomer = "ENOL_KETO"
for i in range(0,100+1):
    file ="cube_001_total_density.cube"
    path ="fitxer.txt"
    folder_1= f"E_field_{i}/{tautomer}/"            # Folder of the  Field_1(Jordi aquesta és la primera carperta que és visitarà)
    folder_2= f"E_field_{i+1}/{tautomer}/"          #Folder of the Field_2 (Jordi aquesta és la segona carpeta que és visitarà)
    os.chdir(folder_1)                                # Changes directory to current folder    ç
    data_1,bb=cube.read_cube_data(file)
    # Raw_data_1 = np.genfromtxt('cube_001_total_density.cube',usecols=(0,1,2,3,4,5),skip_header=32,missing_values='NA',filling_values=np.nan)  #Reads the data of the file and outputs it in an array form
    os.chdir("../../")       #SURFACE DATA OF N
    os.chdir(folder_2)   
    os.system(f"touch fitxer.txt")
    op=open(file='fitxer.txt', mode ="w")
    data_2,bb=cube.read_cube_data(file)      
    # Raw_data_2 = np.genfromtxt('cube_001_total_density.cube',usecols=(0,1,2,3,4,5),skip_header=32,missing_values='NA',filling_values=np.nan) #Reads the data of the file and outputs it in an array form
    difference = data_2 - data_1 #Diference between the two arrays
    cube.write_cube(op,bb,difference, origin=None, comment=None)
    op.close()
    # np.savetxt('difference.txt', difference) #Saves the array into a file 
    os.system(f"head -32 cube_001_total_density.cube >> differ_{i}.cube")  
    os.system(f"tail +33 fitxer.txt >> differ_{i}.cube")   
    os.chdir("../../")                              # Go back to initial directory
    try: os.makedirs(f"E_field_{i+1}/{tautomer}/")     # Make next folder if not present
    except FileExistsError: pass
