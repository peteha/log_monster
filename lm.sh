#!/bin/bash
image_d=$(cat image.txt)
counter=1
while [ $counter -le 10000 ]
do
  curl -k -X POST https://lc1.pggb.net:9543/api/v1/events/ingest/aexample-uuid-4b7a-8b09-fbfac4b46fd9 -d '{"events": [{"fields": [{"name": "hostname", "content": "pi5"},{"name": "message_type", "content": "image"}],"text": "'$image_d'"}]}'
  ((counter++))
done
