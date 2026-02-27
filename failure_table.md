# Phase 03 Failure Table

| Test | What failed | Expected | Actual | Root cause | Fix | Commit |
|------|-------------|----------|--------|------------|-----|--------|
| inputs/test01.in | EOFError crash at end of file | Program exits cleanly | Crash | stdin ended, not handled | try/except EOFError | <hash> |
| ... | ... | ... | ... | ... | ... | ... |