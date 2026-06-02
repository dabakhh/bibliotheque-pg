# ═══════════════════════════════════════════════════════════════════
# app.py — Application de Gestion de Bibliothèque
# Framework : Flask (Python)
# Base de données : MySQL
# Style : Python procédural — pas de classes
# ═══════════════════════════════════════════════════════════════════

from flask import Flask, render_template, request, redirect, url_for
from database import get_connection

app = Flask(__name__)


# ───────────────────────────────────────────────────────
# ROUTE 1 : Accueil — liste de tous les livres
# URL : GET /
# ───────────────────────────────────────────────────────
@app.route("/")
def accueil():
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM livres ORDER BY titre ASC")
    livres = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", livres=livres)


# ───────────────────────────────────────────────────────
# ROUTE 2 : Ajouter un livre
# URL : GET /ajouter  →  afficher le formulaire
# URL : POST /ajouter →  traiter les données du formulaire
# ───────────────────────────────────────────────────────
@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    erreurs = []

    if request.method == "POST":
        titre  = request.form.get("titre",  "").strip()
        auteur = request.form.get("auteur", "").strip()
        annee  = request.form.get("annee",  "").strip()

        if not titre:
            erreurs.append("Le titre est obligatoire.")
        if not auteur:
            erreurs.append("L'auteur est obligatoire.")
        if annee and not annee.isdigit():
            erreurs.append("L'année doit être un nombre entier.")

        if not erreurs:
            annee_val = int(annee) if annee else None
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO livres (titre, auteur, annee) VALUES (%s, %s, %s)",
                (titre, auteur, annee_val)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("accueil"))

    return render_template("ajouter.html", erreurs=erreurs)


# ───────────────────────────────────────────────────────
# ROUTE 3 : Détail d'un livre
# URL : GET /detail/<id>
# ───────────────────────────────────────────────────────
@app.route("/detail/<int:livre_id>")
def detail(livre_id):
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM livres WHERE id = %s", (livre_id,))
    livre  = cursor.fetchone()
    cursor.close()
    conn.close()

    if livre is None:
        return render_template("404.html"), 404

    return render_template("detail.html", livre=livre)


# ───────────────────────────────────────────────────────
# ROUTE 4 : Supprimer un livre
# URL : GET /supprimer/<id>
# ───────────────────────────────────────────────────────
@app.route("/supprimer/<int:livre_id>")
def supprimer(livre_id):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livres WHERE id = %s", (livre_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("accueil"))


# ───────────────────────────────────────────────────────
# Démarrage du serveur
# ───────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)