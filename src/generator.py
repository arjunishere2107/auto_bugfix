
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def clean_code(output: str) -> str:
    """
    Remove triple-backtick code fences from the LLM output.
    """
    output = output.strip()
    if output.startswith("```"):
        # remove first fence
        output = output.split("```", 1)[1]
        # remove second fence if exists
        if "```" in output:
            output = output.rsplit("```", 1)[0]
    return output.strip()

def generate_fix(buggy_code: str, similar_examples: list) -> str:
    examples_text = ""
    for ex in similar_examples:
        examples_text += (
            f"Example buggy code:\n{ex.get('bug_snippet')}\n"
            f"Fixed code:\n{ex.get('fix_snippet')}\n\n"
        )

    prompt = f"""
You are an expert Python programmer.
Given the buggy code below, produce a corrected version of the code only (no explanations).
Do NOT wrap the answer inside ```python or any backticks.

{examples_text}

Buggy code:
{buggy_code}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.0,
    )

    raw = response.choices[0].message.content
    return clean_code(raw)
