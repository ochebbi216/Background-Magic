import os
from PIL import Image
from rembg import remove

def remove_background(input_img_path):
    img = Image.open(input_img_path).convert("RGBA")
    removed_img = remove(img)
    output_img_path = os.path.join("static/outputs", os.path.basename(input_img_path).replace(".png", "_removed-bg.png"))
    removed_img.save(output_img_path, 'PNG')
    return output_img_path

def add_background(image_path, background_color=None, background_image_path=None):
    # Step 1: Remove the background
    removed_bg_path = remove_background(image_path)
    img = Image.open(removed_bg_path).convert("RGBA")
    
    # Step 2: Add the new background
    if background_image_path:
        background = Image.open(background_image_path).convert("RGBA")
        background = background.resize(img.size)  # Ensure it matches the main image size
    elif background_color:
        background = Image.new("RGBA", img.size, background_color)
    else:
        raise ValueError("Specify either a background color or a background image.")
    
    # Composite the images
    combined = Image.alpha_composite(background, img)
    output_img_path = os.path.join("static/outputs", os.path.basename(image_path).replace(".png", "_with_new_background.png"))
    combined.save(output_img_path)
    return output_img_path
