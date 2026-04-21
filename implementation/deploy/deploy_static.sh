#!/usr/bin/env bash
set -euo pipefail
SOURCE_DIR="$(cd "$(dirname "$0")/../output/site" && pwd)"
TARGET_DIR="/var/www/autonomous-seo-ai-farm"
sudo mkdir -p "$TARGET_DIR"
sudo cp -r "$SOURCE_DIR"/* "$TARGET_DIR"/
sudo find "$TARGET_DIR" -type f | sed -n '1,40p'
echo "Deployed static files to $TARGET_DIR"
