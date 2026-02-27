#!/usr/bin/env bash
# Copies charts from experiments/ into site/public/charts/
# Run as prebuild step: npm run sync-content
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SITE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHARTS_SRC="$REPO_ROOT/experiments/prompt-injection-boundary-tags/report/charts"
CHARTS_DST="$SITE_ROOT/public/charts"

mkdir -p "$CHARTS_DST"

# Copy SVG and PNG charts
if [ -d "$CHARTS_SRC" ]; then
  cp "$CHARTS_SRC"/*.svg "$CHARTS_DST/" 2>/dev/null || true
  cp "$CHARTS_SRC"/*.png "$CHARTS_DST/" 2>/dev/null || true
  echo "Synced charts from $CHARTS_SRC"
else
  echo "Warning: Charts directory not found at $CHARTS_SRC"
fi
