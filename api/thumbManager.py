import os
from PIL import Image  # type: ignore
from moviepy import VideoFileClip  # type: ignore
from typing import Dict, Any, List

class ThumbManager:
    THUMBNAIL_SIZES = {
        "small": (84, 84),
        "medium": (175, 175),
        "large": (350, 350),
    }

    def __init__(self, entry: Dict[str, List[str]]):
        """Initialize the ThumbManager with a dictionary of tags."""
        self.thumbs = entry["thumbnail"]
        self.filepath = entry["filepath"]
        
        # Extract the directory from the filepath
        self.directory = os.path.dirname(self.filepath)
        
        # Define the base thumbnail directory
        self.thumb_base_path = os.path.join(self.directory, '.thumb')
        
        # Create the .thumb directory if it doesn't exist
        self.create_thumb_directory()
        
        # Remove the file extension from entry["name"]
        name_without_extension = os.path.splitext(entry['name'])[0]
        
        # Create paths for different thumbnail sizes
        self.thumb_paths = {
            'small': os.path.join(self.thumb_base_path, 'small', f"{name_without_extension}.png"),
            'medium': os.path.join(self.thumb_base_path, 'medium', f"{name_without_extension}.png"),
            'large': os.path.join(self.thumb_base_path, 'large', f"{name_without_extension}.png")
        }

        # Check if thumbnail paths are valid and generate new ones if necessary
        self.check_and_generate_thumbnails()

    def create_thumb_directory(self):
        """Create the .thumb directory and its subdirectories if they do not exist."""
        if not os.path.exists(self.thumb_base_path):
            os.makedirs(self.thumb_base_path)
            os.makedirs(os.path.join(self.thumb_base_path, 'small'))
            os.makedirs(os.path.join(self.thumb_base_path, 'medium'))
            os.makedirs(os.path.join(self.thumb_base_path, 'large'))

    def check_and_generate_thumbnails(self):
        """Check each thumbnail path; if invalid, generate the corresponding thumbnail."""
        for size, path in self.thumb_paths.items():
            # Create the directory for the thumbnail if it doesn't exist
            thumb_dir = os.path.dirname(path)
            if not os.path.exists(thumb_dir):
                os.makedirs(thumb_dir)

            # Check if the thumbnail file exists; if not, generate it
            if not os.path.exists(path):
                self.generate_new_thumbnail(size)


    def generate_new_thumbnail(self, size: str):
        """Generate a new thumbnail for the specified size based on the media type."""
        if self.filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            self.create_image_thumbnails(self.filepath, size)
        elif self.filepath.lower().endswith('.gif'):
            self.create_gif_thumbnails(self.filepath, size)
        elif self.filepath.lower().endswith(('.mp4', '.webm')):
            self.create_video_thumbnails(self.filepath, size)
        else:
            print(f"Unsupported file type for thumbnail generation: {self.filepath}")

    def save_thumbnail(self, image, size_key, output_path):
        """Save a thumbnail for a given image and size."""
        thumbnail = image.copy()
        thumbnail.thumbnail(self.THUMBNAIL_SIZES[size_key])
        thumbnail.save(output_path)

    def create_image_thumbnails(self, image_path, size_key):
        """Generate thumbnails for an image."""
        try:
            with Image.open(image_path) as img:
                self.save_thumbnail(img, size_key, self.thumb_paths[size_key])
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

    def create_gif_thumbnails(self, gif_path, size_key):
        """Generate thumbnails for a GIF (using the first frame)."""
        try:
            with Image.open(gif_path) as gif:
                first_frame = gif.copy()
                self.save_thumbnail(first_frame, size_key, self.thumb_paths[size_key])
        except Exception as e:
            print(f"Error processing GIF {gif_path}: {e}")

    def create_video_thumbnails(self, video_path, size_key):
        """Generate thumbnails for a video (using the first frame)."""
        try:
            clip = VideoFileClip(video_path)
            frame = clip.get_frame(1)  # Get the first frame at 1st second
            img = Image.fromarray(frame)
            self.save_thumbnail(img, size_key, self.thumb_paths[size_key])
            clip.close()
        except Exception as e:
            print(f"Error processing video {video_path}: {e}")
