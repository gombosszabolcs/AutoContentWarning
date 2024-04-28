from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)


@app.route('/api/process_url', methods=['POST'])
def process_url():
    data = request.json
    url = data.get('url', '')
    if not url:
        return jsonify({"message": "Invalid URL"}), 400

    try:
        logging.info("Processing")
        result = subprocess.run(
            ["python3", "subtitle_generator_from_youtube.py", url],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output = result.stdout.decode("utf-8")
        logging.info(output)
        logging.info(type(output))
        decoded_output = json.loads(output)
        logging.info(decoded_output)
        decision = decoded_output.get("decision", "False")
        logging.info(decision)
        if not output:
            print("No output")
            return jsonify({"message": "No output from script"}), 500

        decision_data = json.loads(output)
        decision = decision_data.get("decision", True)

        return jsonify({"message": "Script executed successfully", "decision": decision})

    except subprocess.CalledProcessError as e:
        logging.error("Subprocess error: %s", e.stderr.decode(
            "utf-8"))
    except json.JSONDecodeError as e:
        logging.error("JSON decoding error: %s", e)
    except Exception as e:
        logging.error("General error: %s", e)


if __name__ == '__main__':
    app.run(debug=True)
