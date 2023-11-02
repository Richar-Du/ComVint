import os
import xml.etree.ElementTree as ET
import re
import tqdm
from multiprocessing import Pool
import argparse

def process_image(args, image_file):
    if '.jpg' not in image_file:
        return
    image_path = os.path.join(args.image_dir, image_file)
    annotation_file = image_file.replace('jpg', 'xml')
    annotation_path = os.path.join(args.annotation_dir, annotation_file)
    sentence_file = image_file.replace('jpg', 'txt')
    sentence_path = os.path.join(args.sentence_dir, sentence_file)
    convert_path = os.path.join(args.convert_dir, sentence_file)

    with open(convert_path, 'w') as convert_f:
        root = ET.parse(annotation_path)
        box_dict = {}
        for obj in root.findall('object'):
            names = obj.findall('name')#.text
            for name in names:
                bndbox = obj.find('bndbox')
                if bndbox is not None:
                    xmin = int(bndbox.find('xmin').text)
                    ymin = int(bndbox.find('ymin').text)
                    xmax = int(bndbox.find('xmax').text)
                    ymax = int(bndbox.find('ymax').text)
                    box_dict[name.text] = [xmin, ymin, xmax, ymax]

        def replace_fn(match):
            id = match.group(1)
            category = match.group(2)
            phrase = match.group(3)
            if id in box_dict:
                bbox = box_dict[id]
                return f"{phrase} {bbox}"
            else:
                return phrase

        captions = open(sentence_path).readlines()
        for i in range(len(captions)):
            captions[i] = re.sub(r'\[/EN#(.+?)/(.+?) (.+?)\]', replace_fn, captions[i]).strip()
            convert_f.write(captions[i]+'\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", default="data/flickr30k_entities/flickr30k-images", help="Path to image directory")
    parser.add_argument("--annotation_dir", default="data/flickr30k_entities/Annotations", help="Path to annotation directory")
    parser.add_argument("--sentence_dir", default="data/flickr30k_entities/Sentences", help="Path to sentence directory")
    parser.add_argument("--convert_dir", default="data/flickr30k_entities/Convert", help="Path to convert directory")
    
    args = parser.parse_args()
    
    with Pool(32) as p:
        image_files = os.listdir(args.image_dir)
        list(tqdm.tqdm(p.imap(lambda x: process_image(args, x), image_files), total=len(image_files)))
