import os
import sys
import json
import argparse
import subprocess
import re
import tempfile
import requests

def call_llm(prompt, provider, api_key, model_name=None):
    """
    Calls the specified LLM provider (gemini, openai, or agy) using direct HTTP requests
    or local agy CLI in print mode.
    """
    if provider == "agy":
        fd, prompt_file = tempfile.mkstemp(suffix=".txt", prefix="prompt_temp_")
        os.close(fd)
        try:
            with open(prompt_file, "w", encoding="utf-8") as f:
                f.write(prompt)
        except Exception as e:
            raise RuntimeError(f"Failed to write temporary prompt file: {e}")
            
        meta_prompt = (
            f"Read the instructions and lecture data in the file {prompt_file}. "
            "Follow all the instructions in it to generate the LaTeX lecture notes document, "
            "and print the resulting raw LaTeX code inside a ```latex code block to stdout. "
            "Do not write any files or run any commands; just output the LaTeX code to stdout."
        )
        
        cmd = [
            "agy",
            "--print", meta_prompt,
            "--dangerously-skip-permissions"
        ]
        
        print("Calling LLM via local agy CLI (indirect file-prompt mode)...")
        try:
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                timeout=300
            )
            # Cleanup temp file
            if os.path.exists(prompt_file):
                os.remove(prompt_file)
                
            if res.returncode != 0:
                raise RuntimeError(f"agy CLI failed (exit code {res.returncode}): {res.stderr}")
            return res.stdout
        except Exception as e:
            if os.path.exists(prompt_file):
                os.remove(prompt_file)
            raise RuntimeError(f"Failed to execute agy command: {e}")

    elif provider == "gemini":
        model = model_name or "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.1
            }
        }
        print(f"Calling Gemini API ({model})...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        res_data = response.json()
        try:
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            raise ValueError(f"Unexpected response structure from Gemini API: {res_data}") from e

    elif provider == "openai":
        model = model_name or "gpt-4o"
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }
        print(f"Calling OpenAI API ({model})...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        res_data = response.json()
        try:
            return res_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise ValueError(f"Unexpected response structure from OpenAI API: {res_data}") from e
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

def extract_latex(llm_output):
    """
    Extracts LaTeX content from markdown code blocks if present.
    """
    pattern = r"```(?:latex)?(.*?)```"
    match = re.search(pattern, llm_output, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return llm_output.strip()

def run_latex_compile(latex_dir, filename="lecture.tex", compile_cmd="pdflatex"):
    """
    Compiles LaTeX. Prefers Tectonic (single cross-platform binary, auto-fetches
    packages, no Docker); falls back to a local TeX compiler, then Docker texlive.
    """
    import shutil
    abs_dir = os.path.abspath(latex_dir)
    tex_path = os.path.join(abs_dir, filename)

    # 1) Tectonic (preferred; identical on macOS + Linux)
    if shutil.which("tectonic"):
        print(f"Compiling '{filename}' in '{abs_dir}' via Tectonic...")
        cmd = ["tectonic", "-X", "compile", "--keep-logs", "--outdir", abs_dir, tex_path]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, timeout=300)
            # tectonic prints diagnostics on stderr even on success
            return res.returncode == 0, res.stdout, res.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Tectonic timeout"
        except Exception as e:
            print(f"Tectonic error ({e}); trying next compiler...")

    # 2) Local pdflatex/lualatex
    if shutil.which(compile_cmd):
        print(f"Compiling '{filename}' via local {compile_cmd}...")
        cmd = [compile_cmd, "-interaction=nonstopmode", filename]
        try:
            res = subprocess.run(cmd, cwd=abs_dir, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True, timeout=120)
            return res.returncode == 0, res.stdout, res.stderr
        except Exception as e:
            print(f"Local {compile_cmd} error ({e}); trying Docker...")

    # 3) Docker texlive fallback
    print(f"Compiling '{filename}' in '{abs_dir}' via Docker texlive...")
    cmd = [
        "docker", "run", "--rm", "-v", f"{abs_dir}:/workdir", "-w", "/workdir",
        "texlive/texlive:latest", compile_cmd, "-interaction=nonstopmode", filename,
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True, timeout=120)
        return res.returncode == 0, res.stdout, res.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

def parse_latex_log(log_path):
    """
    Parses the LaTeX log file to extract errors and their line numbers.
    """
    if not os.path.exists(log_path):
        return []
        
    errors = []
    # Match standard LaTeX error line numbers like "l.123"
    line_pattern = re.compile(r"^l\.(\d+)")
    
    # Simple log parser: look for lines starting with "!" and grab following lines
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        if line.startswith("!"):
            error_msg = line.strip()
            line_num = None
            # Scan downstream for the line number (usually within 5 lines)
            for j in range(idx + 1, min(idx + 6, len(lines))):
                match = line_pattern.match(lines[j].strip())
                if match:
                    line_num = int(match.group(1))
                    break
            errors.append({
                "message": error_msg,
                "line": line_num
            })
            
    return errors

def get_line_context(tex_path, line_num, context_window=5):
    """
    Gets the surrounding lines of code for a given line number.
    """
    if not os.path.exists(tex_path) or line_num is None:
        return ""
        
    with open(tex_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    start = max(0, line_num - context_window - 1)
    end = min(len(lines), line_num + context_window)
    
    context = []
    for idx in range(start, end):
        prefix = "-> " if idx == line_num - 1 else "   "
        context.append(f"{idx + 1:4d}:{prefix}{lines[idx]}")
        
    return "".join(context)

def main():
    parser = argparse.ArgumentParser(description="Stage 8 & 9: LLM-Based LaTeX Note Generation and Validation Loop")
    parser.add_argument("--ir", type=str, default="ir/lecture_ir.json", help="Path to lecture_ir.json")
    parser.add_argument("--output-dir", type=str, default="latex", help="Directory to output lecture.tex and lecture.pdf")
    parser.add_argument("--provider", type=str, default="agy", choices=["gemini", "openai", "agy"], help="LLM provider")
    parser.add_argument("--api-key", type=str, default=None, help="LLM API key (falls back to env)")
    parser.add_argument("--model", type=str, default=None, help="LLM Model name")
    parser.add_argument("--compiler", type=str, default="pdflatex", choices=["pdflatex", "lualatex"], help="LaTeX compiler")
    parser.add_argument("--max-retries", type=int, default=5, help="Max compilation correction attempts")
    # Local/cloud backend switching for the generation step
    parser.add_argument("--gen-mode", choices=["local", "cloud"], default="cloud",
                        help="Where the generation model runs")
    parser.add_argument("--gen-base-url", default=None, help="OpenAI-compatible base URL for local generation")
    parser.add_argument("--device", default="auto", choices=["auto", "metal", "cuda", "cpu"])
    parser.add_argument("--main-font", default=None,
                        help="Unicode main font for the XeTeX/Tectonic preamble "
                             "(default: 'Times New Roman' on macOS, 'DejaVu Serif' on Linux)")

    args = parser.parse_args()

    # Pick a Cyrillic-capable Unicode font that exists on the target OS.
    # Tectonic uses XeTeX, so the classic T2A/inputenc/babel route (which needs
    # cm-super metrics Tectonic doesn't bundle) fails; fontspec + a system font works.
    if args.main_font:
        main_font = args.main_font
    elif sys.platform == "darwin":
        main_font = "Times New Roman"
    else:
        main_font = "DejaVu Serif"

    # Build a single generate() callable that hides local-vs-cloud from the loop.
    if args.gen_mode == "local":
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from backends import LLMClient
        client = LLMClient(mode="local", model=args.model, base_url=args.gen_base_url,
                           device=args.device)
        print(f"Generation backend: {client.describe()}")
        generate = lambda p: client.complete(p)
        api_key = None
    else:
        # Get API key for cloud providers
        if args.provider != "agy":
            api_key = args.api_key or (os.environ.get("GEMINI_API_KEY") if args.provider == "gemini" else os.environ.get("OPENAI_API_KEY"))
            if not api_key:
                print(f"Error: API key for {args.provider} must be provided or set in environment variables.")
                sys.exit(1)
        else:
            api_key = None
        generate = lambda p: call_llm(p, args.provider, api_key, args.model)
        
    # Read aligned IR
    with open(args.ir, "r", encoding="utf-8") as f:
        ir_data = json.load(f)
        
    os.makedirs(args.output_dir, exist_ok=True)
    tex_path = os.path.join(args.output_dir, "lecture.tex")
    log_path = os.path.join(args.output_dir, "lecture.log")
    
    # ------------------ STAGE 8: GENERATION ------------------
    print("\n--- Stage 8: Generating LaTeX Lecture Notes via LLM ---")
    
    prompt = f"""
You are a professional mathematician and LaTeX typesetter.
Your goal is to convert a chronological sequence of whiteboard OCR states and aligned speech transcripts from a lecture into a single, cohesive, well-structured, and compilable LaTeX lecture notes document.

Here is the raw lecture data in chronological order:
{json.dumps(ir_data, indent=2, ensure_ascii=False)}

Instructions:
1. Write the lecture notes entirely in Bulgarian, preserving the language of the transcript. Use professional Bulgarian mathematical terminology.
2. Group the content into logical sections and subsections (e.g., \\section{{...}}, \\subsection{{...}}).
3. Do NOT make a frame-by-frame transcript. Write it as a clean, DETAILED textbook chapter or set of lecture notes.
3a. Be thorough and verbose. Aim for comprehensive notes, not a summary. For every concept on the board: state the formal definition, then explain it in prose using the lecturer's spoken intuition from the aligned "speech", and show the reasoning/derivation steps rather than just the final formula. Keep ALL worked examples in full (with the numbers the lecturer used) and add a sentence or two of explanation for each. Where the speech motivates or interprets a formula, include that motivation. Prefer several short paragraphs per subsection over a single dense one. Do not drop content to be concise — completeness matters more than brevity.
4. Merge duplicate or overlapping formulas. Since the blackboard changes over time, some formulas will be repeated or updated. Present them in their final, complete, and correct form (but still show intermediate forms when they illustrate a derivation).
5. Fix any OCR-induced errors in the LaTeX formulas (e.g., mismatched brackets, missing backslashes, wrong characters).
6. Surround math blocks with \\[ ... \\] and inline math with $ ... $.
7. The output must be a single, complete, compilable LaTeX document starting with \\documentclass{{article}} and ending with \\end{{document}}.
8. Use standard math packages: \\usepackage{{amsmath}}, \\usepackage{{amssymb}}, \\usepackage{{amsfonts}}. The document is compiled with Tectonic (XeTeX engine), so for Cyrillic/Bulgarian you MUST use a Unicode/fontspec preamble — NOT inputenc/fontenc/babel. Immediately after \\documentclass, put exactly:
   \\usepackage{{fontspec}}
   \\setmainfont{{{main_font}}}
   Do NOT use \\usepackage[T2A]{{fontenc}}, \\usepackage[utf8]{{inputenc}}, \\usepackage[bulgarian]{{babel}}, or any font package like PTSerif — they break under Tectonic.
9. Each state may carry a "verification" block (SymPy + LLM cross-check). Where it flags an equation as "inconsistent"/"unparsed" or suggests a correction, prefer the corrected/consistent form and silently fix obvious OCR artifacts. Do NOT mention the verification process in the notes.
10. Only return the raw LaTeX code inside a ```latex code block. Do not add any conversational text before or after the block.
"""

    llm_response = generate(prompt)
    latex_code = extract_latex(llm_response)

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_code)
    print(f"LaTeX document generated and saved to {tex_path}")
    
    # ------------------ STAGE 9: VALIDATION LOOP ------------------
    print("\n--- Stage 9: Running LaTeX Validation and Self-Correction Loop ---")
    
    iteration = 1
    while iteration <= args.max_retries:
        print(f"\n[Attempt {iteration}/{args.max_retries}] Compiling LaTeX...")
        success, stdout, stderr = run_latex_compile(args.output_dir, "lecture.tex", args.compiler)
        
        if success:
            print("LaTeX compilation succeeded!")
            print(f"Success! Output PDF is available at {os.path.join(args.output_dir, 'lecture.pdf')}")
            break
        else:
            print("Compilation failed. Parsing log file for errors...")
            errors = parse_latex_log(log_path)
            
            if not errors:
                print("No clear error lines found in log. Full compilation output check needed.")
                # Construct fallback error description
                error_desc = "Unknown error (could be missing package or syntax error). Please check LaTeX document syntax."
                lines_context = ""
                error_line = None
            else:
                first_error = errors[0]
                error_line = first_error["line"]
                error_desc = first_error["message"]
                print(f"Error: {error_desc} near line {error_line}")
                lines_context = get_line_context(tex_path, error_line)
                print(f"Context:\n{lines_context}")
                
            print("Requesting correction from LLM...")
            
            # Read the full .tex file so the LLM can see the entire document
            with open(tex_path, "r", encoding="utf-8") as tf:
                full_tex_contents = tf.read()

            correction_prompt = f"""
The LaTeX compilation failed with the following error:
{error_desc}

{f"The error occurred at or near line {error_line}." if error_line else ""}
Here is the context around the error location:
```latex
{lines_context}
```

Here is the full LaTeX document:
```latex
{full_tex_contents}
```

Please fix the error. Return the COMPLETE, updated, and compilable LaTeX document inside a ```latex code block. Do not include any explanation.
"""
            try:
                llm_response = generate(correction_prompt)
                latex_code = extract_latex(llm_response)
                
                with open(tex_path, "w", encoding="utf-8") as f:
                    f.write(latex_code)
                print(f"LaTeX document updated. Saved to {tex_path}")
            except Exception as e:
                print(f"LLM correction call failed: {e}")
                
            iteration += 1
            
    if iteration > args.max_retries:
        print("\nMax retries reached. Compilation was not successful. Please review lecture.tex manually.")
        sys.exit(1)

if __name__ == "__main__":
    main()
