import os
from PIL import Image, ImageDraw

def create_squircle_icon(src_path, dest_path, size, radius_pct=0.22):
    if not os.path.exists(src_path):
        print(f"Source file not found: {src_path}")
        return False
    
    # Load original transparent logo
    logo = Image.open(src_path).convert("RGBA")
    # Resize logo to target size
    logo = logo.resize((size, size), Image.Resampling.LANCZOS)
    
    # Create white squircle canvas
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    radius = int(size * radius_pct)
    # Draw rounded rectangle (squircle) background
    draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=(255, 255, 255, 255))
    
    # Paste logo on top
    # logo has transparency, so we use it as mask
    canvas.alpha_composite(logo)
    
    # Save the result
    canvas.save(dest_path, "PNG")
    print(f"Created squircle icon: {dest_path} ({size}x{size})")
    return True

def build_all():
    img_dir = r"f:\NEB\backend_python\web\static\web\img"
    src_logo = os.path.join(img_dir, "n-logo-1024.png")
    
    # Check if the source is 1024
    if not os.path.exists(src_logo):
        src_logo = os.path.join(img_dir, "n-logo-512.png")
        if not os.path.exists(src_logo):
            print("No high-res source logo found!")
            return
            
    print(f"Using source logo: {src_logo}")
    
    # Targets
    targets = [
        ("n-logo-1024.png", 1024),
        ("n-logo-512.png", 512),
        ("n-logo-192.png", 192),
        ("n-logo-180.png", 180),
        ("n-logo-32.png", 32),
        ("n-logo-16.png", 16),
    ]
    
    temp_files = []
    for filename, size in targets:
        dest_path = os.path.join(img_dir, filename)
        
        # Backup original transparent file if we want to restore or just overwrite
        # We will overwrite directly as we are updating the icons for deployment.
        create_squircle_icon(src_logo, dest_path, size)
        
    # Generate favicon.ico
    # A standard .ico contains multiple sizes (16, 32, 48)
    ico_sizes = [16, 32, 48]
    ico_frames = []
    
    for size in ico_sizes:
        temp_dest = os.path.join(img_dir, f"temp-ico-{size}.png")
        if create_squircle_icon(src_logo, temp_dest, size):
            ico_frames.append(Image.open(temp_dest))
            temp_files.append(temp_dest)
            
    if ico_frames:
        ico_path = os.path.join(img_dir, "favicon.ico")
        ico_frames[0].save(ico_path, format="ICO", sizes=[(s, s) for s in ico_sizes], append_images=ico_frames[1:])
        print(f"Created favicon.ico: {ico_path}")
        
    # Cleanup temp files
    for temp in temp_files:
        try:
            os.remove(temp)
        except OSError:
            pass

if __name__ == "__main__":
    build_all()
