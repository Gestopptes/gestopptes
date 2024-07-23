#!/bin/bash

set -ex

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve models..."
for model in llama3 llama3-groq-tool-use ; do
    until ollama pull $model; do sleep 15; done
done

echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid