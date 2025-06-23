from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'diagnostico.db'

# Crear la base de datos si no existe
def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE diagnosticos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sintomas TEXT NOT NULL,
                    diagnostico TEXT NOT NULL
                )
            ''')
            conn.commit()

# Función simple de diagnóstico (puedes mejorarla después)
def generar_diagnostico(sintomas):
    sintomas_set = set(sintomas)

    if {"fiebre", "dolor_abdominal", "debilidad", "perdida_apetito"} <= sintomas_set:
        return "Posible fiebre tifoidea. Acuda a un centro de salud para análisis."
    elif {"fiebre", "escalofrios", "sudoracion", "dolor_cabeza"} <= sintomas_set:
        return "Síntomas compatibles con paludismo. Se recomienda prueba rápida de malaria."
    elif {"fiebre", "tos", "dolor_garganta"} <= sintomas_set:
        return "Posible gripe o infección respiratoria."
    elif {"diarrea", "vomitos"} <= sintomas_set:
        return "Podría tratarse de una gastroenteritis."
    elif {"congestion", "estornudos"} <= sintomas_set:
        return "Probablemente una alergia o resfriado común."
    elif {"dificultad_respirar", "fiebre"} <= sintomas_set:
        return "Síntomas compatibles con COVID-19. Consulte a un médico."
    else:
        return "Síntomas no concluyentes. Se recomienda consultar con un profesional."


@app.route('/')
def inicio():
    return redirect(url_for('formulario_sintomas'))

@app.route('/sintomas', methods=['GET'])
def formulario_sintomas():
    return render_template('sintomas.html')

@app.route('/diagnostico', methods=['POST'])
def procesar_formulario():
    sintomas = request.form.getlist('sintomas')
    diagnostico = generar_diagnostico(sintomas)

    # Guardar en la base de datos
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO diagnosticos (sintomas, diagnostico) VALUES (?, ?)",
            (", ".join(sintomas), diagnostico)
        )
        conn.commit()

    return render_template('resultado.html', sintomas=sintomas, diagnostico=diagnostico)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
