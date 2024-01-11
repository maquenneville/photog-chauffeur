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
    image_folder = input("Enter the folder path containing images/videos: ")
    results_folder = input("Enter the folder path for saving search results (to skip, enter 'n'): ")

    while True:
        # Get the search query from the user
        print("""
              Commands:
                  
                  a. Image Search
                  b. Describe Image
                  c. Describe Video
                  
                  enter "exit" to quit program
              """)
        command = input("\nEnter command: ")
        
        if command.lower() == 'exit':
            print("Exiting the program.")
            break
        
        if "a" in command:
            
            query = input("Enter your search query (or type 'exit' to quit): ")
            
            if results_folder == "n":
                
                results_folder = input("Enter the folder path for saving search results: ")
    
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
                
        elif "b" in command:
            
            image_filename = input("Enter the filename and extention (filename.ext) of the image to be described: ")
            
            image_path = image_folder + f"\\{image_filename}"
            
            description = bot.describe_image(image=image_path)
            
            print(f"""Image Description:
                  
                  {description}
                  
                  
                  """)
        
        elif "c" in command:
            
            video_filename = input("Enter the filename and extention (filename.ext) of the video to be described: ")
            
            video_path = image_folder + f"\\{video_filename}"
            
            description = bot.describe_video(video=video_path)
            
            print(f"""Video Description:
                  
                  {description}
                  
                  
                  """)
            
        
        

if __name__ == "__main__":
    main()
