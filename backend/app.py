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
        # Python szkript futtatása az URL-lel
        result = subprocess.run(
            ["python3", "subtitle_generator_from_youtube.py", url],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output = result.stdout.decode("utf-8")
        logging.info(output)
        # logging.info(type(output))
        # decoded_output = json.loads(output)
        # logging.info(decoded_output)
        # decision = decoded_output.get("decision", "False")
        # logging.info(decision)
        if not output:
            print("No output")
            return jsonify({"message": "No output from script"}), 500

        decision_data = json.loads(output)
        decision = decision_data.get("decision", True)

        return jsonify({"message": "Script executed successfully", "decision": decision})

    except subprocess.CalledProcessError as e:
        return jsonify({
            "message": "Error executing script",
            "error": e.stderr.decode("utf-8")
        }), 500

    except json.JSONDecodeError:
        return jsonify({"message": "Invalid JSON output"}), 500

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "Unexpected error", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
