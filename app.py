from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__)
CACHE_FILE = "standings_cache.json"


# ======================================================
# DESACTIVAR CACHÉ PARA TODAS LAS RESPUESTAS (IMPORTANTE)
# ======================================================
@app.after_request
def add_header(response):
    # Esto evita que el navegador o Render cacheen los archivos JSON
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
def index():
    return render_template("index.html")



# ======================================================
# RUTA PARA EL PANEL
# ======================================================
@app.route("/panel")
def panel():
    return render_template("panel.html")



# ======================================================
# ENDPOINT QUE ACTUALIZA adjustments.json
# ======================================================
@app.post("/update-adjustments")
def update_adjustments():
    try:
        payload = request.get_json()

        # Guardar el archivo JSON con indentación
        with open("adjustments.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400



# ======================================================
# API QUE ENTREGA TODA LA DATA PROCESADA
# ======================================================
@app.route("/api/full")
def api_full():
    if not os.path.exists(CACHE_FILE):
        return jsonify({"error": "Data not available yet, please try again in a few minutes."}), 503

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        data["last_updated"] = datetime.fromtimestamp(
            os.path.getmtime(CACHE_FILE)
        ).strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": f"Failed to read cached data: {e}"}), 500



# ======================================================
# RUTA QUE ENTREGA EL adjustments.json REAL DEL SERVIDOR
# ======================================================
@app.route("/adjustments.json")
def serve_adjustments():
    return send_from_directory(".", "adjustments.json")



if __name__ == "__main__":
    app.run(debug=True)
