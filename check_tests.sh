#!/usr/bin/env bash
# CSCI 3060U Phase 3 - Step 6: Validate Results
set -euo pipefail

EXPECTED_DIR="expected"

# Find all input files matching the pattern inputs/*.txt
shopt -s nullglob
inputs=(inputs/*.txt)

echo "Starting output validation..."

# Iterate over each input file...
for infile in "${inputs[@]}"; do
  base=$(basename "$infile" .txt)
  echo "-----------------------------------"
  echo "Checking test: $base"

  # Validate transactions (.atf vs .etf)
  if diff "outputs/${base}.atf" "$EXPECTED_DIR/${base}.etf" > /dev/null; then
    echo "  [PASS] Transactions match."
  else
    echo "  [FAIL] Transactions differ!"
  fi

  # Validate terminal log (.out vs .out)
  if diff "outputs/${base}.out" "$EXPECTED_DIR/${base}.out" > /dev/null; then
    echo "  [PASS] Terminal output matches."
  else
    echo "  [FAIL] Terminal output differs!"
  fi
done

echo "--------------------"
echo "Validation complete."