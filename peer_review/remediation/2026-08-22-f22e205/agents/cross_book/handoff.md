# Cross-book handoff

Completed the shared remediation in [formulas.tex](/Users/g8row/Documents/lec2tex/lectures/bodies/formulas.tex)
and [frontmatter.tex](/Users/g8row/Documents/lec2tex/lectures/bodies/frontmatter.tex) for all 21 assigned
master IDs. The formula sheet now carries certified conditioning, endpoint,
support, a.e./regular-version, moment-existence, Gamma-rate, LLN/CLT/MGF,
pivot/regression, counting, notation, and continuous-distribution-domain
qualifications. Every assigned ID has exactly one `resolved` JSONL record;
lecture-side dependencies are noted there and were remediated by the lecture
owners.

Validation passed: `git diff --check`, JSONL parsing, TeX environment and brace
balance, and targeted label/notation inspection. No global build was run, and
no lecture body, preamble, generated driver, or PDF was edited.
