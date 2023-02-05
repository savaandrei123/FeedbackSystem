from __init__ import db, ma
from Models.programme import Programme, ProgrammeSchema


class Faculty(db.Model):
    __tablename__ = "faculties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    years = db.Column(db.Integer)

    def __init__(self, name: str, years: int):
        self.name = name
        self.years = years

    @staticmethod
    def create(name: str, years: int):
        try:
            new_faculty = Faculty(name, years)
            db.session.add(new_faculty)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update(id: int, new_name: str, new_years: int):
        try:
            faculty = Faculty.query.get(id)
            faculty.name = new_name
            faculty.years = new_years
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete(id: int):
        try:
            Faculty.query.filter(Faculty.id == id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_faculties():
        try:
            faculties = Faculty.query.all()
            faculties_schema = FacultySchema(many=True)
            faculties_list = faculties_schema.dump(faculties)
            return faculties_list
        except Exception as e:
            print(e)
            return "error"

    @staticmethod
    def get_programmes(id: int):
        try:
            programmes = Programme.query.filter(Programme.faculty_id == id)
            programmes_schema = ProgrammeSchema(many=True)
            programmes_list = programmes_schema.dump(programmes)
            return programmes_list
        except Exception as e:
            print(e)
            return "error"

    @staticmethod
    def get_courses(id: int):
        try:
            courses_list = []
            programmes = Faculty.get_programmes(id)
            for prg in programmes:
                prg_courses = Programme.get_courses(prg["id"], 0)
                for course in prg_courses:
                    courses_list.append(course)
            return courses_list
        except Exception as e:
            print(e)
            return "error"

    @staticmethod
    def get_years(id: int):
        try:
            faculty = Faculty.query.filter(Faculty.id == id).first()
            if faculty:
                return faculty.years
        except Exception as e:
            print(e)
            return "error"


class FacultySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Faculty
