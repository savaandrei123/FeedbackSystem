from __init__ import db, ma
from sqlalchemy import ForeignKey
from Models.course import Course, CourseSchema
from Models.programmeCourses import ProgrammeCoursesSchema, ProgrammeCourses


class Programme(db.Model):
    __tablename__ = "programmes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    faculty_id = db.Column(db.Integer, ForeignKey(
        "faculties.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, name: str, faculty_id: int):
        self.name = name
        self.faculty_id = faculty_id

    @staticmethod
    def create(name: str, faculty_id: int):
        try:
            new_prog = Programme(name, faculty_id)
            db.session.add(new_prog)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update(id: int, new_name: str, new_faculty_id: int):
        try:
            programme = Programme.query.get(id)
            programme.name = new_name
            programme.faculty_id = new_faculty_id
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete(id: int):
        try:
            Programme.query.filter(Programme.id == id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_courses(id: int, year: int):
        try:
            ids = Programme.get_courses_ids(id)
            if year == 0:
                courses = Course.query.filter(Course.id.in_(ids)).all()
            else:
                courses = Course.query.filter(
                    Course.id.in_(ids)).filter(Course.year == year).all()
            course_schema = CourseSchema(many=True)
            courses_list = course_schema.dump(courses)
            return courses_list
        except Exception as e:
            print(e)
            return "error"

    @staticmethod
    def get_courses_ids(id: int):
        try:
            ids = []
            courses_id = ProgrammeCourses.query.filter(
                ProgrammeCourses.programme_id == id).all()
            programme_courses_schema = ProgrammeCoursesSchema(many=True)
            courses_id_list = programme_courses_schema.dump(courses_id)
            for relation in courses_id_list:
                ids.append(relation["id"])
            return ids
        except Exception as e:
            print(e)
            return "error"


class ProgrammeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Programme
