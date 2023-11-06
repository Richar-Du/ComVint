#!/bin/bash

python ComVint/dataprocess/convert_flickr30k.py \
  --image_dir="data/flickr30k_entities/flickr30k-images" \
  --annotation_dir="data/flickr30k_entities/Annotations" \
  --sentence_dir="data/flickr30k_entities/Sentences" \
  --convert_dir="data/flickr30k_entities/Convert"
