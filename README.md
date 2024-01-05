# PhotogChauffeur

## Overview
PhotogChauffeur is a Python-based tool that allows users to search through a collection of images in a specified folder using natural language queries. The program utilizes OpenAI's GPT-4 Vision API to interpret the query and return relevant images based on their content. Results can be saved to a designated folder for further use.

## Features
- Image search using natural language queries.
- Support for processing multiple images concurrently.
- Option to save search results to a specified folder.
- User-friendly command-line interface.

## Requirements
- Python 3.11
- OpenAI API key

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
python main.py
```

Follow the on-screen prompts to enter the folder paths and search queries. Type 'exit' to terminate the program.

## License
Distributed under the MIT License. See `LICENSE` for more information.
