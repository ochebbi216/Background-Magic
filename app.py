from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from service import remove_background, add_background

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_and_display():
    if request.method == 'POST':
        file = request.files['image']
        if file.filename == '':
            return "No selected file"

        # Save the uploaded file with a unique timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = f"{secure_filename(file.filename)}_{timestamp}.png"
        input_img_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        file.save(input_img_path)

        # Determine action type
        action = request.form.get("action")
        print(f"Action selected: {action}")  # Debugging line

        output_img_path = None

        if action == "remove_background":
            output_img_path = remove_background(input_img_path)
        
        elif action == "color_background":
            color = request.form.get("background_color")
            print(f"Selected color: {color}")  # Debugging line
            try:
                color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5)) + (255,)
                output_img_path = add_background(input_img_path, background_color=color)
            except Exception as e:
                print(f"Error with color background: {e}")  # Debugging line
        
        elif action == "image_background":
            background_file = request.files.get("background_image")
            if background_file:
                background_img_path = os.path.join(app.config['UPLOAD_FOLDER'], f"bg_{timestamp}.png")
                background_file.save(background_img_path)
                output_img_path = add_background(input_img_path, background_image_path=background_img_path)
        
        # If no output image was created, return an error message
        if output_img_path is None:
            return "Failed to process the image with the selected background option."

        # Generate URLs for template rendering
        original_image_url = url_for('static', filename=f'uploads/{original_filename}')
        output_image_url = url_for('static', filename=f'outputs/{os.path.basename(output_img_path)}')

        return render_template('app.html', original_image=original_image_url, output_image=output_image_url)

    return render_template('app.html')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
