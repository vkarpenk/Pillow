# To run the test, use the following command:
# python test.py <compress_level>
# Example: python test.py 1

from PIL import Image
import sys
import time
import os
import numpy as np

if len(sys.argv) != 2:
    print("Usage: python test.py <compress_level>")
    sys.exit(1)

try:
    compress_level = int(sys.argv[1])
    if compress_level < 0 or compress_level > 9:
        raise ValueError("Compress level must be between 0 and 9")
except ValueError as e:
    print(f"Invalid compress level: {e}")
    sys.exit(1)

height, width = 4000, 10000
blue_color = (255, 0, 0) 
img_array = np.full((height, width, 3), blue_color, dtype=np.uint8)

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
