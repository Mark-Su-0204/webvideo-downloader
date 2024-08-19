import os
import json
import sys
import re
import base64


def filter_har(har_path):
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
        file_dir = './temp'
        file_name = id + '_' + str(start) + '-' + str(end) + '.m4s'
        filePath = os.path.join(file_dir, file_name)
        with open(filePath, 'wb') as f:
            f.write(chunk)

har_path = '../har/1.har'
filter_har(har_path)