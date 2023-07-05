# TFM
Python programs used in the TFM thesis.
This project used these programs to produce results for the electric field section.

The programs are used to generate the files for optimizations with increasing electric fields. The programs on these parts only use modules that come with the normal Python.

The programs used to generate and create the charge density difference. The program that generates charge density difference uses an external module called ASE.

ELECTRIC FIELD GENERATOR

These programs need the first folder made with the geometry, control, and the aims submitting script (you should change the name of the file in the program). The folder name should be named E_field_0. With this program you can add initial_moment by inserting the atom index in the variables list of alpha_carbons_up (if you want an initial_moment 1) or alpha_carbons_down (if you want an initial_moment -1). You can also request to input constrains by adding the index of the desired atoms in the list of constrain_carbons. If you don't want any of these to describe your system you can simply leave them blank . You can change the electric field vector or/and intensity in the function copy files in line 33 of the code.

IMPORTANT YOUR FIRST CALCULATION IN FIELD 0 YOU SHOULD CONSTRUCT THE INPUT OF THE GEOMETRY.

You can run this program by typing: python3 constrain_version.py


CUBE FILES GENERATORS

This program generates cube fields via the geometry fields in folders named E_field_i where i is the step of the electric field. The same principles of the electric field generator are used here. Also here you have to change the name of the aims script for submitting jobs to your own script, as in the electric field generator.

You can run this program by typing :  python3 cube_files_gen3.py


DIFFERENCE GENERATOR

This program generates from the output cubefiles in the folders of format E_field_i where i is the step of the electric field. This program uses the external ASE module.

You can run this program by typing: python3 cube_dif_gen.py


