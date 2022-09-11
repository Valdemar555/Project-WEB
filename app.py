from flask import Flask, render_template, request, redirect
from models import Note, Tag, db_session #Contact,
from datetime import datetime, date

app = Flask(__name__)
app.debug = True
app.env = "development"

@app.route('/', strict_slashes=False)
def index():
    notes = db_session.query(Note).all()
    #contacts = db_session.query(Contact).all()
    
    return render_template('index.html', notes=notes, )#contacts=contacts

@app.route("/delete/note/<id>", strict_slashes=False)
def delete_note(id):
    db_session.query(Note).filter(Note.id == id).delete()
    db_session.commit()

    return redirect("/")

@app.route("/done/<id>", strict_slashes=False)
def done(id):
    db_session.query(Note).filter(Note.id == id).first().done = True
    db_session.commit()
    return redirect("/")

@app.route("/note/", methods=["GET", "POST"], strict_slashes=False)
def add_note():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        tags = request.form.getlist("tags")
        tags_obj = []
        for tag in tags:
            tags_obj.append(db_session.query(Tag).filter(Tag.name == tag).first())
        note = Note(name=name, description=description, tags=tags_obj)
        db_session.add(note)
        db_session.commit()
        return redirect("/")
    else:
        tags = db_session.query(Tag).all()

    return render_template("note.html", tags=tags)


@app.route("/tag/", methods=["GET", "POST"], strict_slashes=False)
def add_tag():
    if request.method == "POST":
        name = request.form.get("name")
        tag = Tag(name=name)
        db_session.add(tag)
        db_session.commit()
        return redirect("/")

    return render_template("tag.html")

@app.route('/edit_note/<id>', methods=['GET', 'PUT'], strict_slashes=False)
def note_edit(id):
    note = db_session.query(Note).filter(Note.id == id).first()
    if request.method == "PUT":
        name = request.form.get("name")
        description = request.form.get("description")
        tags = request.form.getlist("tags")
        tags_obj = []
        for tag in tags:
            tags_obj.append(db_session.query(Tag).filter(Tag.name == tag).first())
        note.name = name
        note.description = description
        note.tags = tags_obj
        db_session.commit()
        return redirect("/")
    else:
        tags = db_session.query(Tag).all()
    return render_template('edit_note.html', tags=tags, note=note)


if __name__ == "__main__":
    app.run()