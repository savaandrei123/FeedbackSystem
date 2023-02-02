from __init__ import db, ma
from datetime import datetime
from sqlalchemy import ForeignKey


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    prof_id = db.Column(db.Integer, ForeignKey(
        "professors.id", ondelete="CASCADE"), nullable=False)
    room = db.Column(db.String)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    day = db.Column(db.Integer)
    week_type = db.Column(db.Integer)
    year = db.Column(db.Integer)

    def __init__(self, name: str, prof_id: int, room: str, start: datetime, end: datetime, day: int, week_type: int, year: int):
        self.name = name
        self.prof_id = prof_id
        self.room = room
        self.start = start
        self.end = end
        self.day = day
        self.week_type = week_type
        self.year=year

    @staticmethod
    def create(name: str, prof_id: int, room: str, start: datetime, end: datetime, day: int, week_type: int, year: int):
        new_course = Course(name, prof_id, room, start, end, day, week_type, year)
        db.session.add(new_course)
        db.session.commit()
        return True

    @staticmethod
    def update(id: int, new_name: str, new_prof_id: int, new_room: str, new_start: datetime, new_end: datetime, new_day: int, new_week_type: int, new_year: int):
        course = Course.query.get(id)
        course.name = new_name
        course.prof_id = new_prof_id
        course.room = new_room
        course.start = new_start
        course.end = new_end
        course.day = new_day
        course.week_type = new_week_type
        course.year = new_year
        db.session.commit()
        return True

    @staticmethod
    def delete(id: int):
        Course.query.filter(Course.id == id).delete()
        db.session.commit()
        return True


class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
