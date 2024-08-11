import os
from pymp4.parser import Box

def parse_m4s(file_path):
    with open(file_path, 'rb') as f:
        while True:
            box = Box.parse_stream(f)
            if box.type == b'moof':
                print(f"Found 'moof' box with length: {len(box)}")
            if f.tell() == len(box):
                break

# 使用示例
temp_dir = '../temp'
file_name = '1'
file_name = file_name + '_video.m4s'

parse_m4s(os.path.join(temp_dir, file_name))