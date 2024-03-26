#!/bin/bash
source /home/colabdev/Desktop/telephone-assistant/openai-env/bin/activate

python /home/colabdev/Desktop/telephone-assistant/embeddings/testing/periodic_API.py & 
python /home/colabdev/Desktop/telephone-assistant/embeddings/testing/stt_embeddings