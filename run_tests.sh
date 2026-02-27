#!/usr/bin/env bash
set -euo pipefail

ACCOUNTS_FILE="accounts.txt"

mkdir -p outputs

shopt -s nullglob
inputs=(inputs/*.txt)
if (( ${#inputs[@]} == 0 )); then
  echo "No input files found in inputs/ (expected inputs/*.txt)"
  exit 1
fi

for infile in "${inputs[@]}"; do
  base=$(basename "$infile" .txt)
  echo "Running $base..."

  # stdout (terminal output) -> outputs/<base>.txt.out
  # transactions file -> outputs/<base>.atf
  python main.py "$ACCOUNTS_FILE" "outputs/${base}.atf" < "$infile" > "outputs/${base}.txt.out"
done

echo "Done. See outputs/ for results."