#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs
fail=0

shopt -s nullglob
expected=(expected_outputs/*)
if (( ${#expected[@]} == 0 )); then
  echo "No expected output files found in expected_outputs/"
  exit 1
fi

for expected_file in "${expected[@]}"; do
  filename=$(basename "$expected_file")

  # If expected is terminal output (.txt), actual is outputs/<base>.txt.out
  if [[ "$filename" == *.txt ]]; then
    base="${filename%.txt}"
    actual="outputs/${base}.txt.out"

  # If expected is transactions (.atf), actual is outputs/<base>.atf
  elif [[ "$filename" == *.atf ]]; then
    base="${filename%.atf}"
    actual="outputs/${base}.atf"

  else
    echo "[SKIP] $filename (unknown expected file extension)"
    continue
  fi

  if [[ ! -f "$actual" ]]; then
    echo "[MISSING] $actual (expected for $filename)"
    fail=1
    continue
  fi

  if diff -u "$expected_file" "$actual" > "outputs/${base}.diff"; then
    echo "[PASS] $filename"
    rm -f "outputs/${base}.diff"
  else
    echo "[FAIL] $filename (see outputs/${base}.diff)"
    fail=1
  fi
done

exit $fail