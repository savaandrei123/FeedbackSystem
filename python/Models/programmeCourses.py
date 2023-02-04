from __init__ import db, ma
from sqlalchemy import ForeignKey


class ProgrammeCourses(db.Model):
    __tablename__ = "programmes_courses"
    id = db.Column(db.Integer, primary_key=True)
    programme_id = db.Column(db.Integer, ForeignKey(
        "programmes.id", ondelete="CASCADE"), nullable=False)
    course_id = db.Column(db.Integer, ForeignKey(
        "courses.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, programme_id: int, course_id: int):
        self.programme_id = programme_id
        self.course_id = course_id

    @staticmethod
    def create(programme_id: int, course_id: int):
        try:
            test = ProgrammeCourses.query.filter(ProgrammeCourses.programme_id == programme_id).filter(
                ProgrammeCourses.course_id == course_id)
            if not db.session.query(test.exists()).scalar():
                new_relationship = ProgrammeCourses(programme_id, course_id)
                db.session.add(new_relationship)
                db.session.commit()
                return True
        except:
            return False

    @staticmethod
    def delete(id: int):
        try:
            ProgrammeCourses.query.filter(ProgrammeCourses.id == id).delete()
            db.session.commit()
            return True
        except:
            return False


class ProgrammeCoursesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProgrammeCourses
