import cv2
import os
import json
from PIL import Image
from PIL.ExifTags import TAGS
import xml.etree.ElementTree as ET

from fractions import Fraction




class ImageViewer:
    def __init__(self, entry):
        
        self.image_data = entry
        self.image_path = entry['filepath']

    def open_image(self):
        # Check if the file exists
        if not os.path.exists(self.image_path):
            print(f"Image file does not exist: {self.image_path}")
            return
        
        # Read the image using OpenCV
        image = cv2.imread(self.image_path)
        if image is None:
            print("Error: Could not open or find the image.")
            return
        
        # Get screen dimensions
        screen_width = 640*2
        screen_height = 480*2

        # Create a resizable window
        cv2.namedWindow(self.image_data['name'], cv2.WINDOW_NORMAL)

        # Set the window size to half of the screen size
        cv2.resizeWindow(self.image_data['name'], screen_width // 2, screen_height // 2)

        # Display the image
        cv2.imshow(self.image_data['name'], image)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()

    def print_metadata(self):
        # Extract metadata using Pillow
        try:
            with Image.open(self.image_path) as img:
                # Print basic image info
                print(f"Format: {img.format}")
                print(f"Mode: {img.mode}")
                print(f"Size: {img.size}")

                # Extract and print EXIF data
                exif_data = img._getexif()
                print(img.info.keys())
                print("AA")
                if exif_data is not None:
                    metadata = {}
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8')  # Decode bytes to string
                            except Exception as e:
                                value = "ERR DECODING"
                        metadata[tag] = value
                    print("EXIF Metadata:")
                    print(metadata)
                else:
                    print("No EXIF metadata found.")
                
                # Extract and print XMP data
                print(img.getxmp())
                xmp_data = img.info.get('xmp', None)
                
                if xmp_data:
                    print("XMP Metadata:")
                    xmp_metadata = self.parse_xmp(xmp_data)
                    print(xmp_metadata)
                    print(json.dumps(xmp_metadata, indent=4))
                else:
                    print("No XMP metadata found.")

                # Extract and print ICC profile
                icc_profile = img.info.get('icc_profile')
                if icc_profile:
                    print("ICC Profile found.")
                else:
                    print("No ICC Profile found.")

                # Extract and print textual metadata (for PNG, etc.)
                text_metadata = img.info.get('text')
                if text_metadata:
                    print("Textual Metadata:")
                    for key, value in text_metadata.items():
                        print(f"{key}: {value}")
                else:
                    print("No textual metadata found.")

        except Exception as e:
            print(f"Error reading metadata: {e}")

    def parse_xmp(self, xmp_data):
        """Parse XMP data and return it as a dictionary."""
        try:
            # Parse the XMP XML data
            root = ET.fromstring(xmp_data)
            xmp_metadata = {}
            for child in root.iter():
                if child.tag.endswith('}'):
                    tag = child.tag.split('}', 1)[1]  # Remove namespace
                else:
                    tag = child.tag
                xmp_metadata[tag] = child.text
            return xmp_metadata
        except ET.ParseError as e:
            print(f"Error parsing XMP data: {e}")
            return {}

    def modify_xmp_subject(self, new_subject):
        """Modify the XMP Subject tag."""
        try:
            with Image.open(self.image_path) as img:
                xmp_data = img.info.get('xml', None)
                if xmp_data:
                    # Parse the existing XMP data
                    root = ET.fromstring(xmp_data)
                    # Find the XMP-dc:subject tag
                    for subject in root.findall('.//{http://purl.org/dc/elements/1.1/}subject'):
                        subject.text = new_subject  # Update the subject text
                    # Convert the modified XML back to a string
                    updated_xmp_data = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
                    # Save the updated XMP data back to the image
                    img.save(self.image_path, xml=updated_xmp_data)
                    print(f"Updated XMP Subject to: {new_subject}")
                else:
                    print("No XMP metadata found to modify.")
        except Exception as e:
            print(f"Error modifying XMP Subject: {e}")

    def modify_metadata(self, key, value):
        # This method can be implemented to modify metadata if needed
        print("Modify metadata functionality is not implemented for image files.")
