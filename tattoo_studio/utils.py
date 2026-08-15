import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

def convert_image_to_webp(image_field, quality=80):
    """
    Converts an uploaded image to WebP format before saving.
    Returns True if converted, False otherwise.
    """
    if not image_field:
        return False
        
    # Only process newly uploaded files, skip already saved ones
    if getattr(image_field, '_committed', True):
        return False

    # Check if a file is actually being uploaded and not just an existing path
    if hasattr(image_field.file, 'name') and image_field.file.name.lower().endswith('.webp'):
        return False

    try:
        # Open image using Pillow
        img = Image.open(image_field)
        
        # Convert to RGB if necessary
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        output = BytesIO()
        img.save(output, format='WEBP', quality=quality)
        output.seek(0)
        
        # Construct the new filename
        clean_name = os.path.basename(image_field.name)
        new_filename = os.path.splitext(clean_name)[0] + '.webp'
        
        # Replace the image field file
        image_field.save(new_filename, ContentFile(output.read()), save=False)
        return True
    except Exception as e:
        print(f"Error converting image to webp: {e}")
        return False
