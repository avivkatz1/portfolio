#!/usr/bin/env bash
# Scaffold a new course folder from templates/course-README.md
# Usage (from portfolio/):  ./scripts/new-course.sh DSC-478 "Programming Machine Learning Applications" "Winter 2027"
set -euo pipefail

if [ $# -lt 3 ]; then
  echo "Usage: $0 <CODE-NUM> \"<Title>\" \"<Term>\"" >&2
  exit 1
fi

CODE="$1"; TITLE="$2"; TERM_NAME="$3"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLUG="$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g')"
DIR="$ROOT/coursework/${CODE}-${SLUG}"

if [ -e "$DIR" ]; then
  echo "Already exists: $DIR" >&2
  exit 1
fi

mkdir -p "$DIR/assignments" "$DIR/final-project"
touch "$DIR/assignments/.gitkeep" "$DIR/final-project/.gitkeep"
sed -e "s|{{CODE}}|${CODE//-/ }|g" -e "s|{{TITLE}}|$TITLE|g" -e "s|{{TERM}}|$TERM_NAME|g" \
  "$ROOT/templates/course-README.md" > "$DIR/README.md"

echo "Created coursework/${CODE}-${SLUG}"
echo "Next: add a row for it in coursework/README.md"
echo "New assignment: mkdir -p \"$DIR/assignments/hw01-topic\"/{notebooks,src,results} && cp \"$ROOT/templates/assignment-README.md\" \"$DIR/assignments/hw01-topic/README.md\""
