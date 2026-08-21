# Remediation queue

This is a planning queue only. No source has been edited. Before any fidelity
change, re-check the relevant transcript/board evidence; do not use
`docs/REMEDIATION.md` as a substitute for that check.

## Q0 — block downstream use first

| Priority | Master IDs | Required disposition |
|---|---|---|
| P0 | ADJ-058 | State that the existing argument proves only the MGF-neighborhood CLT, or replace it with a proof valid under the stated finite-variance hypothesis. Recheck Lecture 13 and formula-sheet reuse at the same time. |

## Q1 — repair P1 claims before adding new exposition

| Cluster | Master IDs | Required disposition |
|---|---|---|
| Models, measures, moments, and boundaries | ADJ-003, ADJ-006, ADJ-010, ADJ-018, ADJ-020, ADJ-022, ADJ-024--ADJ-028, ADJ-041, ADJ-043 | Add exact domains/assumptions and correct historical/model data. Preserve source wording in a note where fidelity requires it, but do not leave false unconditional claims. |
| Conditioning and transformations | ADJ-034, ADJ-037 | Repair zero-denominator/atom formulas and state valid transformation regularity/support assumptions. |
| Limit theorems and inference | ADJ-056--ADJ-061, ADJ-067, ADJ-076--ADJ-077 | Restore iid/nondegeneracy/range assumptions, replace invalid finite-sample normal bounds, and separate one-sample from regression prerequisites. |
| Major fidelity divergence | ADJ-049 | Decide whether the large bounded-triangle example belongs in the book; if retained, label it as supplemental and repair ADJ-045. |

## Q2 — grouped P2 work after Q0/Q1

| Work package | Master IDs |
|---|---|
| Foundations, probability spaces, and early discrete material | ADJ-001, ADJ-002, ADJ-004, ADJ-005, ADJ-007--ADJ-009, ADJ-011--ADJ-013, ADJ-015--ADJ-017, ADJ-019, ADJ-021, ADJ-023 |
| Conditional expectation, distribution formulas, and Lecture 07--10 pedagogy | ADJ-029--ADJ-033, ADJ-035--ADJ-036, ADJ-038--ADJ-040, ADJ-042, ADJ-044--ADJ-048, ADJ-050--ADJ-055 |
| Statistical modelling, confidence procedures, and later-course provenance | ADJ-062--ADJ-066, ADJ-068--ADJ-075, ADJ-078--ADJ-084 |

Within each package, change core lecture statements before the formula appendix,
then re-run consistency checks so the appendix does not reintroduce an omitted
condition.

## Q3 — fidelity/provenance decisions requiring editorial intent

- Clearly label authored supplements, examples, exercises, and source rewrites:
  ADJ-039, ADJ-048, ADJ-049, ADJ-054, ADJ-071, ADJ-081, ADJ-082.
- Restore source caveats or missing context only where full transcript evidence
  supports the restoration: ADJ-008, ADJ-012, ADJ-035, ADJ-036, ADJ-053,
  ADJ-055, ADJ-063.
- Preserve rather than silently replace lecturer-specific conventions. The
  strict-CDF choice is governed by ADJ-R-021.

## Do not auto-action

All items in `REJECTED_OR_DOWNGRADED.jsonl` are either optional P3 clarity
improvements, duplicates, primary-reviewer errors, or insufficient-evidence
claims. In particular, do not revive ADJ-R-010 or ADJ-R-017, and do not treat
the exact unavailable-L15-task enumeration in ADJ-R-028 as established fact.
