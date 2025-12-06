from flask import Flask, render_template, jsonify, request
import json
import os



from datetime import datetime

from flask import send_from_directory







app = Flask(__name__)
CACHE_FILE = "standings_cache.json"

@app.route("/")
def index():
    return render_template("index.html")


# ======================================================
# NUEVO: Ruta para mostrar el panel de ajustes
# ======================================================
@app.route("/panel")
def panel():
    return render_template("panel.html")


# ======================================================
# NUEVO: Endpoint para actualizar adjustments.json
# ======================================================
@app.post("/update-adjustments")
def update_adjustments():
    try:
        payload = request.get_json()

        # Guardar el archivo JSON con indentación bonita
        with open("adjustments.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400



@app.route("/api/full")
def api_full():
    if not os.path.exists(CACHE_FILE):
        return jsonify({"error": "Data not available yet, please try again in a few minutes."}), 503

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Marca de tiempo de última actualización (del archivo)
        data["last_updated"] = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE)).strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Failed to read cached data: {e}"}), 500




@app.route("/adjustments.json")
def serve_adjustments():
    return send_from_directory(".", "adjustments.json")




if __name__ == "__main__":
    app.run(debug=True)
