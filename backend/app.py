from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import logging

# Flask alkalmazás létrehozása és CORS engedélyezése
app = Flask(__name__)
CORS(app)

# Logolási beállítások
logging.basicConfig(level=logging.INFO)

# Útvonal a URL-feldolgozáshoz POST módszerrel


@app.route('/api/process_url', methods=['POST'])
def process_url():
    # JSON formátumú adat kiolvasása
    data = request.json
    url = data.get('url', '')
    # Ha nincs URL, akkor hibával térünk vissza
    if not url:
        return jsonify({"message": "Invalid URL"}), 400

    try:
        logging.info("Processing")
        result = subprocess.run(
            ["python3", "subtitle_generator_from_youtube.py", url],
            capture_output=True,
            text=True
        )

        output = result.stdout
        output = output.split("\n")
        output = output[-2]
        print(output)
        logging.info(output)

        if not output:
            print("No output")
            return jsonify({"message": "No output from script"}), 500

        return jsonify({"message": "Script executed successfully", "decision": str(output)})

    except subprocess.CalledProcessError as e:
        return jsonify({
            "message": "Error executing script",
            "error": e.stderr
        }), 500

    except json.JSONDecodeError:
        return jsonify({"message": "Invalid JSON output"}), 500

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "Unexpected error", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
