#!/bin/bash
mycurl() {
    image_d=$(cat image.txt)
    hn=$(hostname)
    curl -k -X POST https://lc1.pggb.net:9543/api/v1/events/ingest/aexample-uuid-4b7a-8b09-fbfac4b46fd9 -d '{"events": [{"fields": [{"name": "hostname", "content": "'$hn'"},{"name": "message_type", "content": "image"}],"text": "'$image_d'"}]}'
}
export -f mycurl

seq 1000000 | parallel -j0 mycurl