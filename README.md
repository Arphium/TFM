# TFM
Python programms used  in the TFM thesis.
This project used these programs to produce resuts for the electric field section.

The programs used to generate the files for the optimitzations with increasing electric fields. The programs on these part only uses modules that come with the normal Python.

The programs used to generate and create the charge density difference. The program that generates charge density difference uses a external module called ASE.

ELECTRIC FIELD GENERATOR

These programs needs the first folder made with the geometry , control and the aims submitting script (you should change the name of the file in the program). The folder name should be named E_field_0.With this program you can aadd initial_moment by inserting the atom index  in the variables list of alpha_carbons_up (if you want an initial_moment 1) or alpha_carbons_down (if you want an initial_moment -1).You can also request to input constrains by adding the index of the desired atoms in the list of constrain_carbons . If youdon't want any of these to describe your system you can simply left them blank . You can change the electric field vector or/and intensity in the fucntion copy files in line 33 of the code.

IMPORTANT YOUR FIRST CALCULATION IN FIELD 0 YOU SHOULD CONSTRUCT YOURSELF THE INPUT OF THE GEOMETRY.

You can run this program by typing : python3 constrain_version.py


CUBE FILES GENERATORS

This program generates cube fields via the geometry fields in folders named E_field_i where i is the step of the electric field. The same principals of the electric field generator are used here. Also here you have to change the name of the aims script for submiting jobs to your own script, as in the electric field generator.

You can run this program by typing :  python3 cube_files_gen3.py


DIFERENCE GENERATOR

This program generates from the outputed cubefiles in the folders of format E_field_i where i is the step of the electric field . This program uses the external ASE module.

You can run this program by typing : python3 cube_dif_gen.py


