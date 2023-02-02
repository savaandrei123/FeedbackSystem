from __init__ import db, ma
from Models.programme import Programme, ProgrammeSchema


class Faculty(db.Model):
    __tablename__ = "faculties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    years = db.Column(db.Integer)

    def __init__(self, name: str, years : int):
        self.name = name
        self.years = years

    @staticmethod
    def create(name: str, years : int):
        try:
            new_faculty = Faculty(name,years)
            db.session.add(new_faculty)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update(id: int, new_name: str, new_years : int):
        try:
            faculty = Faculty.query.get(id)
            faculty.name = new_name
            faculty.years = new_years
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
    
    @staticmethod
    def get_courses(id: int):
        courses_list = []
        programmes = Faculty.get_programmes(id)
        for prg in programmes:
            prg_courses = Programme.get_courses()
            for course in prg_courses:
                courses_list.append(course)
        return courses_list

    @staticmethod
    def get_years(id:int):
        faculty = Faculty.query.filter(Faculty.id == id)
        if faculty:
            return faculty.years

class FacultySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Faculty

