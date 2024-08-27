import os
import json
import sys
import re
import base64
import subprocess


def filter_har(har_path, m4s_dir='../m4s'):
    # returns unique m4s file IDs
    # normally 1 video + 1 audio
    ids = []

    with open(har_path, 'r') as f:
        har = json.load(f)
    entries = har['log']['entries']

    for entry in entries:
        request = entry['request']
        response = entry['response']
        status = response['status']

        if status != 206:
            continue

        url = request['url']
        reg = r'/([0-9-]+).m4s'
        id = re.search(reg, url).group(1)
        if id not in ids:
            ids.append(id)

        headers = response['headers']
        content_range = None
        for header in headers:
            if header['name'] == 'Content-Range':
                content_range = header['value']
                break
        if content_range == None:
            continue
        reg = r'([0-9]+)-([0-9]+)/([0-9]+)'
        search = re.search(reg, content_range)
        start = int(search.group(1))
        end = int(search.group(2))
        total = int(search.group(3))

        content = response['content']
        text = None
        if content != None and 'mimeType' in content and 'text' in content:
            mimeType = content['mimeType']
            if mimeType == 'video/mp4':
                text = content['text']

        if text == None:
            continue
        chunk = base64.b64decode(text)

        file_dir = id
        if not os.path.exists(os.path.join(m4s_dir, file_dir)):
            os.makedirs(os.path.join(m4s_dir, file_dir))
        file_name = str(start) + '-' + str(end) + '.m4s'
        file_path = os.path.join(m4s_dir, file_dir, file_name)
        with open(file_path, 'wb') as f:
            f.write(chunk)

    return ids


def merge_m4s_files(part1_path, part2_path, output_path):
    # 打开第一个文件并读取内容
    with open(part1_path, 'rb') as part1:
        part1_content = part1.read()

    # 打开第二个文件并读取内容
    with open(part2_path, 'rb') as part2:
        part2_content = part2.read()

    # 合并两个部分并写入输出文件
    with open(output_path, 'wb') as output_file:
        output_file.write(part1_content)
        output_file.write(part2_content)


def parse_chunk_from_har(har_path, m4s_dir='../m4s', output_dir='../manifests/Bilibili'):
    ids = filter_har(har_path, m4s_dir)
    for id in ids:
        files = os.listdir(os.path.join(m4s_dir, id))
        headers = [file for file in files if file.startswith('0-')]
        header_path = os.path.join(m4s_dir, id, headers[0])

        for file in files:
            if not file.endswith('.m4s') or file.startswith('0-'):
                continue
            file_path = os.path.join(m4s_dir, id, file)
            
            if not os.path.exists('./temp'):
                os.mkdir('./temp')
            merge_m4s_files(header_path, file_path, './temp/merged.m4s')

            if not os.path.exists(os.path.join(output_dir, id)):
                os.makedirs(os.path.join(output_dir, id))
            output_path = os.path.join(output_dir, id, file[:-4])

            cmd = 'ffmpeg -y -i ./temp/merged.m4s -c copy ./temp/merged.mp4 2> ' + output_path
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            



parse_chunk_from_har('../har/2.har')

# merge_m4s_files('../m4s/1654848578-1-30280/0-1401.m4s', '../m4s/1654848578-1-30280/89377-188683.m4s', 'merged.m4s')
# har_path = '../har/3.har'
# filter_har(har_path)
