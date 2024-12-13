import os
from PIL import Image  # type: ignore
from moviepy import VideoFileClip  # type: ignore

# Define thumbnail sizes
THUMBNAIL_SIZES = {
    "small": (84, 84),
    "medium": (175, 175),
    "large": (350, 350),
}

def save_thumbnail(image, size_key, output_dir, base_name):
    """Save a thumbnail for a given image and size."""
    thumbnail = image.copy()
    thumbnail.thumbnail(THUMBNAIL_SIZES[size_key])
    output_path = os.path.join(output_dir, f"{base_name}.png")
    thumbnail.save(output_path)

def create_image_thumbnails(image_path, output_dirs):
    """Generate thumbnails for an image."""
    try:
        with Image.open(image_path) as img:
            base_name = os.path.basename(image_path)
            for size_key, output_dir in output_dirs.items():
                save_thumbnail(img, size_key, output_dir, base_name)
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

def create_gif_thumbnails(gif_path, output_dirs):
    """Generate thumbnails for a GIF (using the first frame)."""
    try:
        with Image.open(gif_path) as gif:
            first_frame = gif.copy()
            base_name = os.path.basename(gif_path)
            for size_key, output_dir in output_dirs.items():
                save_thumbnail(first_frame, size_key, output_dir, base_name)
    except Exception as e:
        print(f"Error processing GIF {gif_path}: {e}")

def create_video_thumbnails(video_path, output_dirs):
    """Generate thumbnails for a video (using the first frame)."""
    try:
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(1)  # Get the first frame at 1st second
        img = Image.fromarray(frame)
        base_name = os.path.basename(video_path)
        for size_key, output_dir in output_dirs.items():
            save_thumbnail(img, size_key, output_dir, base_name)
        clip.close()
    except Exception as e:
        print(f"Error processing video {video_path}: {e}")

def process_media_files(input_dir, output_dirs):
    """Process all media files in a directory."""
    for output_dir in output_dirs.values():
        os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            create_image_thumbnails(file_path, output_dirs)
        elif file_name.lower().endswith('.gif'):
            create_gif_thumbnails(file_path, output_dirs)
        elif file_name.lower().endswith(('.mp4', '.webm')):
            create_video_thumbnails(file_path, output_dirs)
        else:
            print(f"Unsupported file type: {file_name}")

if __name__ == "__main__":
    input_directory = "C:/Users/Valerii/Documents/localbooru/temp"
    output_directories = {
        "small": "C:/Users/Valerii/Documents/localbooru/thumb/small",
        "medium": "C:/Users/Valerii/Documents/localbooru/thumb/medium",
        "large": "C:/Users/Valerii/Documents/localbooru/thumb/large",
    }

    process_media_files(input_directory, output_directories)