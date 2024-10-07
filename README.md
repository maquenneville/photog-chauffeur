# PhotogChauffeur

## Overview
PhotogChauffeur is a Python-based tool that allows users to search through a collection of images in a specified folder using natural language queries. The program utilizes OpenAI's GPT-4 Vision API to visualize the input images and return relevant images based on the query. Results can be saved to a designated folder for further use.  Also has features for image and video description generation.

#### Example Search Phrases:

- "Which images have more than one person in them?"
- "Show me all images with dim lighting."
- "Provide me with all images where people are wearing hats."
- "Which of these images do you think is best?"

## Features
- Image search using natural language queries
- Support for processing multiple images concurrently
- Option to save search results to a specified folder
- High-detail image description
- Video description utilizing frame sampling

## Requirements
- Python 3.11
- OpenAI API key for a Plus account

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/maquenneville/PhotogChauffeur.git
   ```
2. Navigate to the cloned repository:
   ```
   cd PhotogChauffeur
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Update the config.ini file with your personal OpenAI API key

## Usage
Run the program using Python:

```
python vision_search_ui.py
```

Follow the on-screen prompts to enter the folder paths, queries, image and video files. Type 'exit' to terminate the program.

## Limitations
This tool is not perfect at applying the search query, and is only as powerful as the machine vision capabilities of gpt-4o.  It may take multiple attempts with different phrasing, or simply not be able to find images with certain parameters.  Experiment to find what works best.

## Upcoming Features
- [x] Image description for single images 
- [x] Video description using a sample of frames
- [ ] Iterative search, allowing the user to filter photos further after the initial search

## License
Distributed under the MIT License. See `LICENSE` for more information.
