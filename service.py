import os
from PIL import Image
from rembg import remove

def remove_background(input_img_path):
    # Generate the expected output path
    output_img_path = os.path.join("static/outputs", os.path.basename(input_img_path).replace(".png", "_removed-bg.png"))
    
    # Check if the file already exists
    if os.path.exists(output_img_path):
        return output_img_path  # Return the existing file path

    # Process image if output file doesn't exist
    img = Image.open(input_img_path).convert("RGBA")
    removed_img = remove(img)
    removed_img.save(output_img_path, 'PNG')
    return output_img_path

def add_background(image_path, background_color=None, background_image_path=None):
    # Generate the expected output path
    suffix = "_with_color_bg.png" if background_color else "_with_image_bg.png"
    output_img_path = os.path.join("static/outputs", os.path.basename(image_path).replace(".png", suffix))

    # Check if the file already exists
    if os.path.exists(output_img_path):
        return output_img_path  # Return the existing file path

    # Process if output file doesn't exist
    removed_bg_path = remove_background(image_path)
    img = Image.open(removed_bg_path).convert("RGBA")

    # Set up the new background
    if background_image_path:
        background = Image.open(background_image_path).convert("RGBA")
        background = background.resize(img.size)  # Ensure it matches the main image size
    elif background_color:
        background = Image.new("RGBA", img.size, background_color)
    else:
        raise ValueError("Specify either a background color or a background image.")
    
    # Composite and save the result
    combined = Image.alpha_composite(background, img)
    combined.save(output_img_path)
    return output_img_path
