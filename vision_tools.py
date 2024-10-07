# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 23:41:12 2024

@author: marca
"""

import os
import shutil

def copy_found_images(filenames, source_folder, output_folder):
    """
    Copy specified files from the source folder to the output folder.

    :param filenames: List of filenames to be copied.
    :param source_folder: Path to the source folder containing the files.
    :param output_folder: Path to the output folder where files will be copied.
    """
    # Ensure the output folder exists, create if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Copy each file from the source to the output folder
    for filename in filenames:
        source_file = os.path.join(source_folder, filename)
        output_file = os.path.join(output_folder, filename)

        # Check if the file exists in the source folder
        if os.path.exists(source_file):
            shutil.copy2(source_file, output_file)
            #print(f"Copied '{filename}' to '{output_folder}'.")
        else:
            print(f"File '{filename}' not found in '{source_folder}'.")
    print(f"images saved to {output_folder}")
