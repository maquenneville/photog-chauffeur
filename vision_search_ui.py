# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 20:16:43 2023

@author: marca
"""

from image_describer import MachineVisionBot
from vision_tools import copy_found_images
import json

def main():
    # Create an instance of the MachineVisionBot
    bot = MachineVisionBot()

    # Get the folder paths from the user
    image_folder = input("Enter the folder path containing images: ")
    results_folder = input("Enter the folder path for saving search results: ")

    while True:
        # Get the search query from the user
        query = input("Enter your search query (or type 'exit' to quit): ")
        
        if query.lower() == 'exit':
            print("Exiting the program.")
            break

        try:
            # Use the bot to visualize and search within multiple images
            search_result = bot.visualize_multiple_images(image_folder, query, search=True)

            # Print the search result in JSON format
            print(json.dumps(search_result, indent=4))

            # Ask user if they want to save the search results
            save_results = input("Do you want to save these search results? (y/n): ").lower()
            if save_results == 'y':
                if 'search_results' in search_result:
                    filenames = search_result['search_results']
                    copy_found_images(filenames, image_folder, results_folder)
                else:
                    print("No valid search results to save.")
            else:
                print("Search results not saved.")

        except Exception as e:
            print(f"An error occurred during the search: {e}")
        
        

if __name__ == "__main__":
    main()
