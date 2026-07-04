from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import sys, os, tempfile

# ── make sure src/ is importable ──
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.detector  import run_pylint
from src.retriever import query_similar
from src.generator import generate_fix
from src.validator import apply_fix_and_test

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path="/"
)

CORS(app, origins="*", allow_headers="*", methods=["GET", "POST", "OPTIONS"])


@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")


@app.route("/api/fix", methods=["POST", "OPTIONS"])
def fix_code():
    if request.method == "OPTIONS":
        return "", 200

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if not file.filename.endswith(".py"):
        return jsonify({"error": "Only .py files are supported"}), 400

    code = file.read().decode("utf-8")

    # ── write to system temp folder so Flask reloader doesn't detect it ──
    temp_path = Path(tempfile.gettempdir()) / "bugagent_temp.py"
    temp_path.write_text(code)

    try:
        msgs       = run_pylint(str(temp_path))
        sim        = query_similar(code)
        fixed_code = generate_fix(code, sim)
        ok, logs   = apply_fix_and_test(temp_path, fixed_code, None)

        return jsonify({
            "success":     ok,
            "original":    code,
            "fixed":       fixed_code,
            "pylint_msgs": msgs,
            "logs":        logs,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # use_reloader=False ← stops Flask restarting when temp files change
    app.run(debug=True, port=8501, host="0.0.0.0", use_reloader=False)