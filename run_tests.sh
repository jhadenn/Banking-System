#!/usr/bin/env bash
# CSCI 3060U Phase 3 - Step 5: Run Tests
set -euo pipefail

ACCOUNTS_FILE="accounts.txt"
mkdir -p outputs

shopt -s nullglob
# Paths to input files
inputs=(inputs/*.txt)

echo "Starting test execution..."

# Iterate over each input file...
for infile in "${inputs[@]}"; do
  base=$(basename "$infile" .txt)
  echo "-----------------------------------"
  echo "Running test: $base"

  # Run program and capture both the .atf transaction file and the .out terminal log
  python main.py "$ACCOUNTS_FILE" "outputs/${base}.atf" < "$infile" > "outputs/${base}.out"
  
  echo "  [DONE] Generated outputs/${base}.atf and outputs/${base}.out"
done

echo "-----------------------------------"
echo "Execution complete. Run ./check_tests.sh to validate."