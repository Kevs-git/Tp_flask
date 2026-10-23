taches = [
{"id": 1, "titre": "Réviser les décorateurs", "priorite": "haute", "terminee": False},
{"id": 2, "titre": "Installer Flask", "priorite": "normale", "terminee": True},
{"id": 3, "titre": "<b>Important</b>", "priorite": "basse", "terminee": False},
]



from flask import Flask, abort, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

app.secret_key = "0000000000"

@app.route("/")
def index():
    filtre = request.args.get("filtre")
    if filtre is None:
        filtre = session.get("filtre", "toutes")
    else:
        session["filtre"] = filtre  
    
    if filtre == "actives":
        taches_filtrees = [t for t in taches if not t["terminee"]]
    elif filtre == "terminees":
        taches_filtrees = [t for t in taches if t["terminee"]]
    else:
        taches_filtrees = taches

    return render_template("taches.html", taches=taches_filtrees, filtre_actuel=filtre)

@app.route("/taches/<int:id>")
def tache (id):
    print(type(int), id)
    for t in taches:
        if t["id"] == id:
            return t["titre"]
    abort (404)
    
@app.route("/taches/ajouter", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        titre = request.form.get("titre", "").strip()
        priorite = request.form.get("priorite", "normale")
        nouvel_id = max((t["id"] for t in taches), default=0) + 1
        taches.append({"id": nouvel_id, "titre": titre,
            "priorite": priorite, "terminee": False})
        flash("Tâche ajoutée")
        return redirect(url_for("index"))
    
    return render_template("ajouter.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("Bonus404.html"), 404
    
