# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 23:15:56 2023

@author: marca
"""

import openai
from openai import OpenAI
#from openai.error import RateLimitError, InvalidRequestError, APIError, OpenAIError
import time
import configparser
import tiktoken
import base64
import random
import cv2
from math import ceil
import os
import json
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError
from concurrent.futures import ThreadPoolExecutor
import io
import shutil






normal_prompt = "Generate a compelling, highly detailed description of the provided image."


class MachineVisionBot:
    
    def __init__(self, image_prompt=None, video_prompt=None):
        self.openai_api_key = self._get_api_keys("config.ini")
        openai.api_key = self.openai_api_key
        self.client = OpenAI(api_key=self.openai_api_key)
        self.model = "gpt-4o"
        
        if image_prompt:
            self.image_prompt = image_prompt
        else:
            self.image_prompt = "Generate a compelling, highly detailed description of the provided image."
            
        if video_prompt:
            self.video_prompt = video_prompt
        else:
            self.video_prompt = "These are frames from a video. Using these frames as a reference, generate a compelling, highly detailed description of the video.  I'm aware that you cannot process video directly, however using these images you can give an accurate description of the video.  Therefore, act as if you can directly process video.  Do not reference the frames, or how they only imply what the video is about, simply provide the description of the video to the best of your ability."


    def _get_api_keys(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        openai_api_key = config.get("API_KEYS", "OpenAI_API_KEY")
        return openai_api_key

    def count_image_tokens(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise Exception(f"Unable to read image from {image_path}")

        height, width, _ = image.shape
        return self._count_total_tokens(width, height)
    
    def count_video_tokens(self, video_path, frame_skip=50):
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise Exception(f"Unable to open video from {video_path}")
    
        total_tokens = 0
        frame_count = 0
    
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            if frame_count % frame_skip == 0:
                height, width, _ = frame.shape
                total_tokens += self._count_total_tokens(width, height)
            frame_count += 1
    
        video.release()
        return total_tokens

    def _count_total_tokens(self, width, height):
        n = ceil(width / 512) * ceil(height / 512)
        total = 85 + 170 * n
        return total
    
    def _encode_image(self, image_path, max_length=512):

        with Image.open(image_path) as img:
            # Calculate the target size while maintaining aspect ratio
            ratio = min(max_length / img.width, max_length / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))

            # Resize the image using LANCZOS resampling filter
            img.thumbnail(new_size, Image.Resampling.LANCZOS)

            # Encode the resized image to base64
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

            return encoded_image
        
    def _encode_video_frames(self, video_path, frame_skip):
        video = cv2.VideoCapture(video_path)
        base64_frames = []
        frame_count = 0

        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            if frame_count % frame_skip == 0:
                _, buffer = cv2.imencode('.jpg', frame)
                base64_frames.append(base64.b64encode(buffer).decode('utf-8'))
            frame_count += 1

        video.release()
        return base64_frames
    
    def _find_and_convert_json(self, input_string):
        # Regex pattern to find strings that look like JSON objects
        json_pattern = r'\{.*?\}'
        
        matches = re.findall(json_pattern, input_string, re.DOTALL)
    
        for match in matches:
            try:
                json_object = json.loads(match)
                return json_object  # Return the first valid JSON object found
            except json.JSONDecodeError:
                continue  # If it's not valid JSON, move to the next match
    
        return None  # Return None if no valid JSON object is found
    
    def _is_image_file(self, file_path):
        try:
            with Image.open(file_path) as img:
                return True
        except UnidentifiedImageError:
            return False
        
    def _cleanup_temp_images(self, folder_path):
        """Delete the entire folder and its contents, then recreate the folder."""
        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
            os.makedirs(folder_path)  # Recreate the folder for future use
        except Exception as e:
            print(f"Failed to cleanup the folder {folder_path}. Reason: {e}")
    
# =============================================================================
#     def add_filename_label_to_image(self, image_path):
#         font_path = "C:\\Windows\\Fonts\\arial.ttf"  # Arial font path for Windows
#         temp_images_folder = "temp_images"  # Name of the temporary images folder
# 
#         try:
#             # Ensure the temp_images folder exists
#             if not os.path.exists(temp_images_folder):
#                 os.makedirs(temp_images_folder)
# 
#             with Image.open(image_path) as img:
#                 draw = ImageDraw.Draw(img)
# 
#                 # Extract filename with extension
#                 filename = os.path.basename(image_path)
# 
#                 # Calculate font size as a proportion of image width
#                 font_size = int(img.width / 30)  # Adjust the ratio as needed
#                 font = ImageFont.truetype(font_path, font_size)
# 
#                 # Calculate text width and height using textbbox
#                 text_bbox = draw.textbbox((0, 0), filename, font=font)
#                 text_width = text_bbox[2] - text_bbox[0]
#                 text_height = text_bbox[3] - text_bbox[1]
# 
#                 # Adjust text_position to move the label up and to the left
#                 offset = 20  # Pixels to move the label up and to the left, adjust as needed
#                 text_position = (img.width - text_width - offset, img.height - text_height - (offset + 20))
# 
#                 draw.text(text_position, filename, font=font, fill=(255, 255, 255))  # White text
# 
#                 # Generate the new file name in the temp_images folder
#                 base = os.path.basename(image_path).split('.')[0]
#                 ext = os.path.splitext(image_path)[1]
#                 labeled_image_path = os.path.join(temp_images_folder, f"{base}_labeled{ext}")
# 
#                 # Save the edited image in the temp_images folder
#                 img.save(labeled_image_path)
# 
#                 return labeled_image_path
# 
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return None
# =============================================================================
        
    def add_filename_label_to_image(self, image_path):
        font_path = "C:\\Windows\\Fonts\\arial.ttf"  # Arial font path for Windows
        temp_images_folder = "temp_images"  # Name of the temporary images folder

        try:
            # Ensure the temp_images folder exists
            if not os.path.exists(temp_images_folder):
                os.makedirs(temp_images_folder)

            with Image.open(image_path) as img:
                draw = ImageDraw.Draw(img)

                # Extract filename with extension
                filename = os.path.basename(image_path)

                # Calculate font size as a proportion of image width
                font_size = int(img.width / 30)  # Adjust the ratio as needed
                font = ImageFont.truetype(font_path, font_size)

                # Calculate text width and height using textbbox
                text_bbox = draw.textbbox((0, 0), filename, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                # Adjust text_position to move the label up and to the left
                offset = 20  # Pixels to move the label up and to the left, adjust as needed
                text_position = (img.width - text_width - offset, img.height - text_height - (offset + 20))

                # Draw text with black border
                border_offset = 10 # Adjust for thicker or thinner border
                for dx in range(-border_offset, border_offset + 1):
                    for dy in range(-border_offset, border_offset + 1):
                        draw.text((text_position[0] + dx, text_position[1] + dy), filename, font=font, fill=(0, 0, 0))  # Black text (border)

                draw.text(text_position, filename, font=font, fill=(255, 255, 255))  # White text (center)

                # Generate the new file name in the temp_images folder
                base = os.path.basename(image_path).split('.')[0]
                ext = os.path.splitext(image_path)[1]
                labeled_image_path = os.path.join(temp_images_folder, f"{base}_labeled{ext}")

                # Save the edited image in the temp_images folder
                img.save(labeled_image_path)

                return labeled_image_path

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def label_images_in_folder_concurrently(self, folder_path):
        # Get all files in the folder and filter out non-image files
        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                       if os.path.isfile(os.path.join(folder_path, f)) and self._is_image_file(os.path.join(folder_path, f))]

        # Use ThreadPoolExecutor to process images concurrently
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.add_filename_label_to_image, image_path) for image_path in image_files]
            labeled_images = [future.result() for future in futures]

        return labeled_images
        
    def describe_image(self, image):
        encoded_image = self._encode_image(image)
        retry_attempts = 0
        max_retries = 5  # You can adjust this as needed
        backoff_factor = 2
        prompt = self.image_prompt
        
        
        max_tokens = 4090


        while retry_attempts < max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                            ]
                        }
                    ],
                    max_tokens=max_tokens
                )

                return response.choices[0].message.content

            except Exception as e:
                if 'rate limit' in str(e):
                    time_to_wait = (backoff_factor ** retry_attempts) + random.uniform(0, 1)
                    print(f"Rate limit hit, waiting {time_to_wait} seconds to retry...")
                    time.sleep(time_to_wait)
                    retry_attempts += 1
                    if retry_attempts >= max_retries:
                        raise Exception("Max retries reached for rate limit errors.")
                else:
                    raise e


# =============================================================================
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 break
# =============================================================================
            
            
    def visualize_multiple_images(self, folder_path, prompt, search=False):
        temp_images_folder = "temp_images"  # Define the temp_images folder

        try:
            # Label all images in the folder concurrently
            self.label_images_in_folder_concurrently(folder_path)
            
            # Encode labeled images
            encoded_images = [self._encode_image(os.path.join(temp_images_folder, f))
                              for f in os.listdir(temp_images_folder)
                              if os.path.isfile(os.path.join(temp_images_folder, f))]

            if search:
                prompt = f"Search Query: {prompt}" + """
                
                Use the filename labels present in the bottom left corner of each image to provide file names that fit the search parameters best. Ensure that the results of this search are returned in valid JSON containing the file names of the search result images, with this format:
                    {
                        "search_results": [list of file names as string values]
                    }
                
                If none of the images fit the search, return the correct JSON object with an empty array value for "search_results".
                """

            retry_attempts = 0
            max_retries = 5
            backoff_factor = 2
            max_tokens = 4090  # Adjust as needed
            
            while retry_attempts < max_retries:
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    *map(lambda x: {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{x}"}}, encoded_images)
                                ]
                            }
                        ],
                        max_tokens=max_tokens
                    )

                    if search:
                        result = self._find_and_convert_json(response.choices[0].message.content)
                    else:
                        result = response.choices[0].message.content

                except Exception as e:
                    if 'rate limit' in str(e):
                        time_to_wait = (backoff_factor ** retry_attempts) + random.uniform(0, 1)
                        print(f"Rate limit hit, waiting {time_to_wait} seconds to retry...")
                        time.sleep(time_to_wait)
                        retry_attempts += 1
                        if retry_attempts >= max_retries:
                            raise Exception("Max retries reached for rate limit errors.")
                    else:
                        raise e

# =============================================================================
#                 except Exception as e:
#                     print(f"An error occurred: {e}")
#                     break
# =============================================================================

                finally:
                    # Cleanup: Delete all files in the temp_images folder
                    self._cleanup_temp_images(temp_images_folder)

                if retry_attempts < max_retries:
                    return result

            return None

        finally:
            # Final Cleanup: Ensure all files in the temp_images folder are deleted
            self._cleanup_temp_images(temp_images_folder)
        

    def describe_video(self, video, frame_skip=50):
        base64_frames = self._encode_video_frames(video, frame_skip)
        retry_attempts = 0
        max_retries = 5
        backoff_factor = 2
        prompt = self.video_prompt
        
        token_ceiling = 4090
        
        max_tokens = 4090
        

        while retry_attempts < max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                *map(lambda x: {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{x}"}}, base64_frames)
                            ]
                        }
                    ],
                    max_tokens=max_tokens
                )

                return response.choices[0].message.content

            except Exception as e:
                if 'rate limit' in str(e):
                    time_to_wait = (backoff_factor ** retry_attempts) + random.uniform(0, 1)
                    print(f"Rate limit hit, waiting {time_to_wait} seconds to retry...")
                    time.sleep(time_to_wait)
                    retry_attempts += 1
                    if retry_attempts >= max_retries:
                        raise Exception("Max retries reached for rate limit errors.")
                else:
                    raise e

# =============================================================================
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 break
# =============================================================================
            
            
#descriptor = MachineVisionBot()

#print(descriptor.describe_image(image=r"C:\Users\marca\Pictures\Saved Pictures\DSC02309.JPG"))

#print(descriptor.visualize_multiple_images_new(folder_path=r"C:\Users\marca\Desktop\Coding\AI\General Classes\test_images", prompt="Show me all images that have more than one person in them.", search=True))

#print(descriptor.describe_video(video=r"C:\Users\marca\Desktop\Coding\AI\General Classes\test_images\F9406C67B0B2_20231126_54-fb16cadf.mp4"))

#descriptor.add_filename_label_to_image(image_path=r"C:\Users\marca\Desktop\Coding\AI\General Classes\test_images\DSC02312.JPG")

#descriptor.label_images_in_folder_concurrently(folder_path=r"C:\Users\marca\Desktop\Coding\AI\General Classes\test_images")

#descriptor.add_filename_label_to_image(image_path=r"C:\Users\marca\Desktop\Coding\AI\MachineVision\search_results\DSC02347.JPG")