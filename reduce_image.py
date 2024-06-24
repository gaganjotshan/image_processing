from PIL import Image
import io
import os

def reduce_image_size(input_path, output_path, max_size_kb=1000, quality=95):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Open the image
    with Image.open(input_path) as img:
        # Convert to RGB if it's not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Start with original size
        width, height = img.size
        
        while True:
            # Save the image to a bytes buffer
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            
            # Check if the size is within the limit
            if buffer.tell() <= max_size_kb * 1024:
                with open(output_path, 'wb') as f:
                    f.write(buffer.getvalue())
                print(f"Image saved. Size: {buffer.tell() / 1024:.2f} KB")
                break
            
            # If not, reduce the size by 10%
            width = int(width * 0.9)
            height = int(height * 0.9)
            img = img.resize((width, height), Image.LANCZOS)
            
            # If we've reduced too much, lower the quality instead
            if width < 100 or height < 100:
                quality -= 5
                if quality < 20:
                    print("Cannot reduce further without significant quality loss.")
                    break
                img = Image.open(input_path)  # Start over with original image
                width, height = img.size

# Usage
if __name__ == "__main__":
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct full paths for input and output
    input_path = os.path.join(script_dir, 'input_images', 'input_image.jpg')
    output_path = os.path.join(script_dir, 'output_images', 'output_image.jpg')
    
    reduce_image_size(input_path, output_path, max_size_kb=1000)