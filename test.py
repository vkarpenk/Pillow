# To run the test, use the following command:
# python test.py <compress_level>
# Example: python test.py 1

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import sys
import time
import os
import numpy as np
from io import BytesIO
import requests

if len(sys.argv) != 2:
    print("Usage: python test.py <compress_level>")
    sys.exit(1)

try:
    compress_level = int(sys.argv[1])
except ValueError as e:
    print(f"Invalid compress level: {e}")
    sys.exit(1)

image_url = "https://images.pexels.com/photos/31384129/pexels-photo-31384129/free-photo-of-bustling-urban-street-in-tokyo-japan.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
response = requests.get(image_url)
if response.status_code != 200:
    print("Failed to download the image.")
    sys.exit(1)

img = Image.open(BytesIO(response.content))
img_array = np.array(img)

original_file = 'test_image_original.png'
with open(original_file, 'wb') as f:
    f.write(img_array.tobytes())

original_size = os.path.getsize(original_file)

img = Image.fromarray(img_array)
start_time = time.time()
compressed_file = 'test_image_compressed.png'
img.save(compressed_file, format='PNG', compress_level=compress_level)
end_time = time.time()

compressed_size = os.path.getsize(compressed_file)

decompress_start_time = time.time()
decompressed_img = Image.open(compressed_file)
decompressed_img.load()
decompress_end_time = time.time()

print("Compression level:", compress_level)
print(f"Original size: {original_size} bytes")
print(f"Compressed size: {compressed_size} bytes")
compression_ratio = ((original_size - compressed_size) / original_size) * 100
print(f"Compression ratio: {compression_ratio:.2f}%")
print(f"Compression time: {end_time - start_time:.2f} seconds")
print(f"Decompression time: {decompress_end_time - decompress_start_time:.2f} seconds")
