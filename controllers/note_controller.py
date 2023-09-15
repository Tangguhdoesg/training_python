from flask import abort
from models.note_model import Note, NoteSchema
from models.person_model import Person, PersonSchema

def read_all():
    notes = Note.query.outerjoin(Person).all()

    note_schema = NoteSchema(many = True)
    results = note_schema.dump(notes)

    return results

def create(person_id, note):
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )

    if person is None:
        abort(
            404,
            f"Person with id {person_id} is not found"
        )
    else:
        content = note.get('content')
        new_note = Note(content = content, person_id = person.person_id)
        person.notes.append(new_note)
        person.create_note()

        note_schema = NoteSchema()
        result = note_schema.dump(new_note)
        return result

def read_one(person_id, note_id):
    note = (
        Note.query.filter(Note.note_id == note_id)
        .outerjoin(Person, Person.person_id == person_id)
        .one_or_none()
    )

    if note is None:
        abort(
            404,
            f"Note with id {note_id} owned by person with id {person_id} is not found"
        )
    else:
        note_schema = NoteSchema()
        result = note_schema.dump(note)
        return result
    
def update(person_id, note_id, note):
    updated_note = (
        Note.query.filter(Note.note_id == note_id)
        .outerjoin(Person, Person.person_id == person_id)
        .one_or_none()
    )

    if updated_note is None:
        abort(
            404,
            f"Note with id {note_id} owned by person with id {person_id} is not found"
        )
    else:
        note_schema = NoteSchema()
        content = note.get('content')
        update = updated_note.update(content)
        return note_schema.dump(update)

def delete():
    pass
