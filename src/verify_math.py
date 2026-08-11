"""
Stage 5 (NEW): Math verification — SymPy + reasoning-LLM cross-check.

Runs AFTER temporal alignment, over ir/lecture_ir.json. For each aligned state:

  1. SymPy pass  — try to parse every equation's LaTeX; for equations of the
     form `LHS = RHS`, attempt a symbolic/numeric equality check. Unparseable or
     inconsistent equations are flagged (a parse failure is a soft flag: the
     board math may simply use notation SymPy can't read).
  2. LLM pass    — a reasoning model reconciles the board equations against the
     aligned Bulgarian `speech`, flagging contradictions and likely OCR artifacts.

A `verification` block is appended to each state in-place, so the generation
stage can see what to trust / fix.
"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backends import LLMClient, add_backend_args


def _sympy_check(latex_str):
    """Return (status, detail). status in {ok, unparsed, inconsistent}."""
    try:
        from sympy.parsing.latex import parse_latex
        from sympy import simplify, Eq
    except Exception as e:
        return "unparsed", f"sympy/latex parser unavailable: {e}"

    s = (latex_str or "").strip()
    if not s:
        return "unparsed", "empty"
    # Only equalities can be symbolically checked; single expressions just parse.
    try:
        if "=" in s and s.count("=") == 1 and "\\leq" not in s and "\\geq" not in s \
                and "\\neq" not in s and "<" not in s and ">" not in s:
            lhs_s, rhs_s = s.split("=", 1)
            lhs = parse_latex(lhs_s)
            rhs = parse_latex(rhs_s)
            try:
                diff = simplify(lhs - rhs)
                if diff == 0:
                    return "ok", "identity holds"
                # Non-zero could just mean symbolic (e.g. a definition); only
                # flag when both sides are fully numeric.
                if not diff.free_symbols and diff != 0:
                    return "inconsistent", f"{lhs} != {rhs} (diff={diff})"
                return "ok", "parsed (symbolic, not a numeric identity)"
            except Exception:
                return "ok", "parsed (equality, not simplifiable)"
        else:
            parse_latex(s)
            return "ok", "parsed"
    except Exception as e:
        return "unparsed", str(e)[:200]


def _llm_cross_check(state, client):
    equations = [b.get("latex", "") for b in state.get("board_items", [])
                 if b.get("type") == "equation"]
    if not equations:
        return None
    speech = state.get("speech", "")
    prompt = (
        "You are checking OCR of a Bulgarian math lecture whiteboard against the "
        "lecturer's speech for that moment.\n\n"
        f"Board equations (LaTeX):\n" + "\n".join(f"- {e}" for e in equations) + "\n\n"
        f"Lecturer's speech (Bulgarian):\n{speech}\n\n"
        "Return ONLY a JSON object:\n"
        '{"issues": [{"equation": "<latex>", "problem": "<short>", '
        '"suggestion": "<corrected latex or null>"}], "confidence": "high|medium|low"}\n'
        "Flag only clear OCR errors or contradictions with the speech. "
        "If everything is consistent, return {\"issues\": [], \"confidence\": \"high\"}."
    )
    try:
        raw = client.complete(prompt)
        raw = raw.strip()
        if "```" in raw:
            import re
            m = re.search(r"```(?:json)?\s*(.*?)```", raw, re.DOTALL)
            if m:
                raw = m.group(1).strip()
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end != -1:
            raw = raw[start:end + 1]
        return json.loads(raw)
    except Exception as e:
        return {"issues": [], "confidence": "low", "error": str(e)[:200]}


def verify(ir_path, client=None, use_llm=True):
    with open(ir_path, "r", encoding="utf-8") as f:
        ir = json.load(f)

    total_eq = total_flagged = 0
    for state in ir:
        sym_results = []
        for b in state.get("board_items", []):
            if b.get("type") != "equation":
                continue
            total_eq += 1
            status, detail = _sympy_check(b.get("latex", ""))
            if status != "ok":
                total_flagged += 1
            sym_results.append({"latex": b.get("latex", ""),
                                "sympy_status": status, "detail": detail})

        verification = {"sympy": sym_results}
        if use_llm and client is not None:
            llm = _llm_cross_check(state, client)
            if llm is not None:
                verification["llm"] = llm
        state["verification"] = verification

    with open(ir_path, "w", encoding="utf-8") as f:
        json.dump(ir, f, ensure_ascii=False, indent=2)

    print(f"Verification complete: {total_eq} equations checked, "
          f"{total_flagged} flagged by SymPy. Report written into {ir_path}.")
    return ir


def main():
    p = argparse.ArgumentParser(description="Stage 5: SymPy + LLM math verification")
    p.add_argument("--ir", default="ir/lecture_ir.json")
    p.add_argument("--no-llm", action="store_true", help="SymPy only, skip the LLM cross-check")
    p.add_argument("--device", default="auto", choices=["auto", "metal", "cuda", "cpu"])
    add_backend_args(p, "verify")
    args = p.parse_args()

    client = None
    if not args.no_llm:
        client = LLMClient(
            mode=args.verify_mode or "local",
            model=args.verify_model,
            base_url=args.verify_base_url,
            provider=args.verify_provider or "agy",
            device=args.device,
        )
        print(f"Verify LLM backend: {client.describe()}")
    verify(args.ir, client=client, use_llm=not args.no_llm)


if __name__ == "__main__":
    main()
