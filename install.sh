#!/bin/sh

curl -s "https://raw.githubusercontent.com/Alyetama/detox/main/detox.py" --output "/usr/local/bin/detox"
chmod +x "/usr/local/bin/detox"
echo "Installed detox successfully!"

detox --help
