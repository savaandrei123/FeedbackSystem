from __init__ import db, ma
from Models.programme import Programme, ProgrammeSchema


class Faculty(db.Model):
    __tablename__ = "faculties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def create(name: str):
        try:
            new_faculty = Faculty(name)
            db.session.add(new_faculty)
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def update(id: int, new_name: str):
        try:
            faculty = Faculty.query.get(id)
            faculty.name = new_name
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def delete(id: int):
        try:
            Faculty.query.filter(Faculty.id == id).delete()
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def get_faculties():
        faculties = Faculty.query.all()
        faculties_schema = FacultySchema(many=True)
        faculties_list = faculties_schema.dump(faculties)
        return faculties_list

    @staticmethod
    def get_programmes(id: int):
        programmes = Programme.query.filter(Programme.faculty_id == id)
        programmes_schema = ProgrammeSchema(many=True)
        programmes_list = programmes_schema.dump(programmes)
        return programmes_list


class FacultySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Faculty
