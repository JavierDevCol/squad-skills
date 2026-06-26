#!/bin/bash
set -e

# --- Help ---
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
  cat <<'EOF'
Usage: scripts/generate_pdf.sh INPUT_FILE [OUTPUT_FILE]

Render a Mermaid diagram (.mmd) to PDF using the Mermaid CLI (mmdc).

Arguments:
  INPUT_FILE    Path to a .mmd file containing Mermaid code (required).
  OUTPUT_FILE   Output file path (default: diagram.pdf).

Examples:
  bash scripts/generate_pdf.sh diagram.mmd output.pdf
  bash scripts/generate_pdf.sh temp.mmd

Requires: @mermaid-js/mermaid-cli (mmdc). Falls back to npx if not installed globally.
EOF
  exit 0
fi

# --- Validation ---
INPUT_FILE="$1"
OUTPUT_FILE="${2:-diagram.pdf}"

if [ -z "$INPUT_FILE" ]; then
  echo "Error: INPUT_FILE is required." >&2
  echo "Usage: scripts/generate_pdf.sh INPUT_FILE [OUTPUT_FILE]" >&2
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File not found: $INPUT_FILE" >&2
  exit 1
fi

# --- Resolve mmdc ---
if command -v mmdc &> /dev/null; then
  MMDC="mmdc"
else
  echo "mmdc not found globally, using npx @mermaid-js/mermaid-cli..." >&2
  MMDC="npx -y -p @mermaid-js/mermaid-cli mmdc"
fi

# --- Generate ---
echo "Generating: $OUTPUT_FILE..." >&2
$MMDC -i "$INPUT_FILE" -o "$OUTPUT_FILE" -b transparent
echo "Done: $OUTPUT_FILE" >&2
