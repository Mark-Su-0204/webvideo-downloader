import os
import json
import m3u8
from matplotlib import pyplot as plt
from matplotlib import font_manager

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


# Input: path to m3u8 file
# Output: m3u8.M3U8
def extract_m3u8(filepath):
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


def draw_chunk_distribution(videos, names, graph_dir, category, app):
    if len(videos) == 0:
        return
    positions = [i for i in range(len(videos))]
    plt.violinplot(videos, positions=positions, showmeans=True)
    plt.title('Violin Plot Example')
    plt.xlabel('Name')
    plt.ylabel('Chunk lengths')
    # plt.xticks(positions, names)
    filepath = os.path.join(graph_dir, app + '_' + category + '.pdf')
    plt.savefig(filepath)
    plt.clf()


def draw_category(app_dir, category, app):
    dir = os.path.join(app_dir, category)
    manifests = sorted(os.listdir(dir))
    videos = []
    names = []
    for manifest in manifests:
        if not manifest.endswith('m3u8'):
            continue
        path = os.path.join(dir, manifest)
        video = parse_m3u8(extract_m3u8(path))
        name = manifest[:-5]
        name = name.split('_')[-1]
        videos.append(video)
        names.append(name)
    draw_chunk_distribution(videos, names, graph_dir, category, app)


app = 'Tencent'
graph_dir = '../graph/chunk_dist'
app_dir = '../manifests/' + app
categories = os.listdir(app_dir)
for category in categories:
    if category == '.DS_Store':
        continue
    draw_category(app_dir, category, app)