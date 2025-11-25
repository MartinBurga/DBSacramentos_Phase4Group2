# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection
from collections import Counter


app = Flask(__name__)
app.secret_key = "clave_super_secreta"  # Necesario para usar flash()

@app.route("/")
def listar_catequizandos():
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT idCatequizando, nombre, apellido, cedula,
               fechaNacimiento, detalles, idNivel
        FROM Catequizando
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    # Resumen
    total = len(rows)
    niveles_counter = Counter()

    for r in rows:
        if r.idNivel is not None:
            niveles_counter[r.idNivel] += 1

    # Convertimos a lista de tuplas (nivel, cantidad) para la plantilla
    niveles_resumen = sorted(niveles_counter.items())

    return render_template(
        "listar_catequizandos.html",
        catequizandos=rows,
        total=total,
        niveles_resumen=niveles_resumen
    )
# CREAR catequizando (GET = form, POST = guardar)
@app.route("/nuevo", methods=["GET", "POST"])
def nuevo_catequizando():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        cedula = request.form.get("cedula")
        fechaNacimiento = request.form.get("fechaNacimiento")
        detalles = request.form.get("detalles")
        idNivel = request.form.get("idNivel") or None

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO Catequizando
            (nombre, apellido, cedula, fechaNacimiento, detalles, idNivel)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(sql, (nombre, apellido, cedula, fechaNacimiento, detalles, idNivel))
        conn.commit()
        conn.close()

        flash("Catequizando creado correctamente.")
        return redirect(url_for("listar_catequizandos"))

    return render_template("formulario_catequizando.html", accion="Nuevo")

# EDITAR catequizando
@app.route("/editar/<int:idCatequizando>", methods=["GET", "POST"])
def editar_catequizando(idCatequizando):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        cedula = request.form.get("cedula")
        fechaNacimiento = request.form.get("fechaNacimiento")
        detalles = request.form.get("detalles")
        idNivel = request.form.get("idNivel") or None

        sql_update = """
            UPDATE Catequizando
            SET nombre = ?, apellido = ?, cedula = ?, fechaNacimiento = ?,
                detalles = ?, idNivel = ?
            WHERE idCatequizando = ?
        """
        cursor.execute(sql_update, (nombre, apellido, cedula, fechaNacimiento,
                                    detalles, idNivel, idCatequizando))
        conn.commit()
        conn.close()

        flash("Catequizando actualizado correctamente.")
        return redirect(url_for("listar_catequizandos"))

    # GET → cargar datos actuales en el formulario
    sql_select = """
        SELECT idCatequizando, nombre, apellido, cedula,
               fechaNacimiento, detalles, idNivel
        FROM Catequizando
        WHERE idCatequizando = ?
    """
    cursor.execute(sql_select, (idCatequizando,))
    catequizando = cursor.fetchone()
    conn.close()

    return render_template("formulario_catequizando.html",
                           accion="Editar",
                           catequizando=catequizando)

# ELIMINAR catequizando
@app.route("/eliminar/<int:idCatequizando>", methods=["POST"])
def eliminar_catequizando(idCatequizando):
    conn = get_connection()
    cursor = conn.cursor()

    sql_delete = "DELETE FROM Catequizando WHERE idCatequizando = ?"
    cursor.execute(sql_delete, (idCatequizando,))
    conn.commit()
    conn.close()

    flash("Catequizando eliminado correctamente.")
    return redirect(url_for("listar_catequizandos"))

if __name__ == "__main__":
    app.run(debug=True)
