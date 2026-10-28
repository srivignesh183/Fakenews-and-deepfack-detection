import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ExifTags

os.makedirs("samples", exist_ok=True)

# 1. Authentic Nature Photograph sample (with EXIF tags simulated, natural optical gradients and noise)
img_authentic = Image.new("RGB", (400, 300), color=(135, 206, 235))
draw = ImageDraw.Draw(img_authentic)
draw.ellipse([280, 40, 360, 120], fill=(255, 223, 0)) # Sun
draw.polygon([(0, 300), (120, 180), (250, 300)], fill=(34, 139, 34)) # Mountain 1
draw.polygon([(180, 300), (300, 150), (400, 300)], fill=(46, 160, 60)) # Mountain 2
arr = np.array(img_authentic, dtype=np.float32)
noise = np.random.normal(0, 4.0, arr.shape)
arr_noisy = np.clip(arr + noise, 0, 255).astype(np.uint8)
img_authentic = Image.fromarray(arr_noisy)

# Save with standard digital camera EXIF metadata
exif_obj = Image.Exif()
exif_obj[0x010f] = "Canon"  # Make
exif_obj[0x0110] = "Canon EOS 80D" # Model
exif_obj[0x0131] = "Ver 1.0.2" # Software / Firmware
img_authentic.save("samples/authentic_sample.jpg", "JPEG", quality=92, exif=exif_obj)

# 2. Manipulated / Spliced Composite Image
# Base realistic photo, then heavily spliced with high-frequency pasted element and Photoshop tag
img_manip = Image.new("RGB", (400, 300), color=(100, 140, 180))
d2 = ImageDraw.Draw(img_manip)
d2.rectangle([40, 40, 360, 260], fill=(130, 170, 210))
# Spliced anomaly patch with sharply divergent noise and synthetic edges
spliced_patch = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
img_patch = Image.fromarray(spliced_patch)
img_manip.paste(img_patch, (150, 100))

# Save with editing software tag
exif_manip = Image.Exif()
exif_manip[0x0131] = "Adobe Photoshop 2024 (Windows)"
img_manip.save("samples/manipulated_sample.jpg", "JPEG", quality=85, exif=exif_manip)

# 3. Synthetic / AI-Generated Deepfake pattern (latent diffusion checkerboard artifacts + zero EXIF)
synthetic_arr = np.zeros((300, 300, 3), dtype=np.uint8)
for i in range(300):
    for j in range(300):
        # High frequency sine wave grid characteristic of checkerboard generator artifacts
        v = int(127 + 120 * np.sin(i / 1.5) * np.cos(j / 1.5))
        synthetic_arr[i, j] = [v, int(v * 0.7), int(255 - v * 0.5)]
img_synthetic = Image.fromarray(synthetic_arr)
# Synthetic images lack EXIF and have extreme spectral frequency peaks
img_synthetic.save("samples/synthetic_sample.jpg", "JPEG", quality=90)

print("Regenerated samples with realistic forensic profiles.")
