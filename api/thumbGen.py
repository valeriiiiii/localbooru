import os
from PIL import Image
from moviepy import VideoFileClip

# Define thumbnail sizes
thumbnail_sizes = {
    "small": (84, 84),
    "medium": (175, 175),
    "large": (350, 350),
}

def create_image_thumbnails(image_path, output_dir_small, output_dir_medium, output_dir_large):
    """Generate thumbnails for an image."""
    try:
        with Image.open(image_path) as img:
            # Make a copy of the image
            thumbnail = img.copy()
            # Resize the image while maintaining aspect ratio
            thumbnail.thumbnail(thumbnail_sizes['small'])
            # Save the thumbnail
            output_path_small = os.path.join(output_dir_small, f"{os.path.basename(image_path)}.png")
            thumbnail.save(output_path_small)

            thumbnail = img.copy()
            thumbnail.thumbnail(thumbnail_sizes['medium'])
            output_path_medium = os.path.join(output_dir_medium, f"{os.path.basename(image_path)}.png")
            thumbnail.save(output_path_medium)

            thumbnail = img.copy()
            thumbnail.thumbnail(thumbnail_sizes['large'])
            output_path_large = os.path.join(output_dir_large, f"{os.path.basename(image_path)}.png")
            thumbnail.save(output_path_large)
            #print(f"Saved {output_path}")
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

def create_gif_thumbnails(gif_path, output_dir_small, output_dir_medium, output_dir_large):
    """Generate thumbnails for a GIF (using the first frame)."""
    try:
        with Image.open(gif_path) as gif:
            # Extract the first frame
            first_frame = gif.copy()
            thumbnail = first_frame.copy()
            thumbnail.thumbnail(thumbnail_sizes['small'])
            # Save the thumbnail
            output_path_small = os.path.join(output_dir_small, f"{os.path.basename(gif_path)}.png")
            thumbnail.save(output_path_small)

            first_frame = gif.copy()
            thumbnail = first_frame.copy()
            thumbnail.thumbnail(thumbnail_sizes['medium'])
            output_path_medium = os.path.join(output_dir_medium, f"{os.path.basename(gif_path)}.png")
            thumbnail.save(output_path_medium)

            first_frame = gif.copy()
            thumbnail = first_frame.copy()
            thumbnail.thumbnail(thumbnail_sizes['large'])
            output_path_large = os.path.join(output_dir_large, f"{os.path.basename(gif_path)}.png")
            thumbnail.save(output_path_large)
            #print(f"Saved {output_path}")
    except Exception as e:
        print(f"Error processing GIF {gif_path}: {e}")

def create_video_thumbnails(video_path, output_dir_small, output_dir_medium, output_dir_large):
    """Generate thumbnails for a video (using the first frame)."""
    try:
        clip = VideoFileClip(video_path)
        # Extract the first frame
        frame = clip.get_frame(1)  # Get the first frame at 1st seconds
        # Convert to PIL image
        img = Image.fromarray(frame)
        thumbnail = img.copy()
        thumbnail.thumbnail(thumbnail_sizes['small'])
        # Save the thumbnail
        output_path_small = os.path.join(output_dir_small, f"{os.path.basename(video_path)}.png")
        thumbnail.save(output_path_small)

        clip = VideoFileClip(video_path)
        # Extract the first frame
        frame = clip.get_frame(1)  # Get the first frame at 1st seconds
        # Convert to PIL image
        img = Image.fromarray(frame)
        thumbnail = img.copy()
        thumbnail.thumbnail(thumbnail_sizes['medium'])
        output_path_medium = os.path.join(output_dir_medium, f"{os.path.basename(video_path)}.png")
        thumbnail.save(output_path_medium)

        clip = VideoFileClip(video_path)
        # Extract the first frame
        frame = clip.get_frame(1)  # Get the first frame at 1st seconds
        # Convert to PIL image
        img = Image.fromarray(frame)
        thumbnail = img.copy()
        thumbnail.thumbnail(thumbnail_sizes['large'])
        output_path_large = os.path.join(output_dir_large, f"{os.path.basename(video_path)}.png")
        thumbnail.save(output_path_large)
        #print(f"Saved {output_path}")
        clip.close()
    except Exception as e:
        print(f"Error processing video {video_path}: {e}")

def process_media_files(input_dir, output_dir_small, output_dir_medium, output_dir_large):
    """Process all media files in a directory."""
    os.makedirs(output_dir_small, exist_ok=True)
    os.makedirs(output_dir_medium, exist_ok=True)
    os.makedirs(output_dir_large, exist_ok=True)
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            create_image_thumbnails(file_path, output_dir_small, output_dir_medium, output_dir_large)
        elif file_name.lower().endswith('.gif'):
            create_gif_thumbnails(file_path, output_dir_small, output_dir_medium, output_dir_large)
        elif file_name.lower().endswith(('.mp4', '.webm')):
            create_video_thumbnails(file_path, output_dir_small, output_dir_medium, output_dir_large)
        else:
            print(f"Unsupported file type: {file_name}")


input_directory = "C:/Users/Valerii/Documents/localbooru/temp"
output_directory_small = "C:/Users/Valerii/Documents/localbooru/thumb/small"
output_directory_medium = "C:/Users/Valerii/Documents/localbooru/thumb/medium"
output_directory_large = "C:/Users/Valerii/Documents/localbooru/thumb/large"

process_media_files(input_directory, output_directory_small, output_directory_medium, output_directory_large)

