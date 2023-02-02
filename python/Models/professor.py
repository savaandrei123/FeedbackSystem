from __init__ import db, ma
from Models.course import Course, CourseSchema


class Professor(db.Model):
    __tablename__ = "professors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def create(name: str):
        try:
            new_prof = Professor(name)
            db.session.add(new_prof)
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def update(id: int, new_name: str):
        try:
            professor = Professor.query.get(id)
            professor.name = new_name
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def delete(id: int):
        try:
            Professor.query.filter(Professor.id == id).delete()
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def get_courses(id: int):
        courses = Course.query.filter(Course.prof_id == id)
        courses_schema = CourseSchema(many=True)
        courses_list = courses_schema.dump(courses)
        return courses_list

    @staticmethod
    def get_professors():
        professors = Professor.query.all()
        professor_schema = ProfessorSchema(many=True)
        professors_list = professor_schema.dump(professors)
        return professors_list

    @staticmethod
    def get_course_professor(id: int):
        professor = Professor.query.filter(Professor.id == id)
        professor_schema = ProfessorSchema()
        professor_list = professor_schema.dump(professor)
        return professor_list

class ProfessorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Professor
