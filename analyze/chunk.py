import os
import json
import m3u8

# Recursively find all values with a certain key name in json
def find_key_in_json(json_data, target_key, res):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == target_key:
                res.append(value)
            find_key_in_json(value, target_key, res)
    
    elif isinstance(json_data, list):
        for item in json_data:
            find_key_in_json(item, target_key, res)

    return res


# For IQY, content of the m3u8 file is contained in json
# Input: path to json file
# Output: m3u8.M3U8
def extract_m3u8_iqy(filepath):
    with open(filepath, 'r') as f:
        j = json.load(f)
    manifest = find_key_in_json(j, 'm3u8', [])
    manifest = m3u8.loads(manifest[0])
    return manifest


# For Tencent, the m3u8 file is pre-downloaded
# Input: path to m3u8 file
# Output: m3u8.M3U8
def extract_m3u8_tencent(filepath):
    with open(filepath, 'r') as f:
        manifest = f.read()
    manifest = m3u8.loads(manifest)
    return manifest

    
# Parse the duration of each chunk
def parse_m3u8(manifest:m3u8.M3U8):
    chunks = []
    for chunk in manifest.segments:
        chunks.append(chunk.duration)
    return chunks


filepath = '../requests/dash.json'
filepath = '../requests/gzc_1000035_0bc3fuaqaaab3aacqpvhaztjilodaawqcaca.f306310.ts.m3u8'
manifest = extract_m3u8_tencent(filepath)
chunks = parse_m3u8(manifest)
print(chunks)
