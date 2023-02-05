from __init__ import db, ma
from datetime import datetime, timedelta
from Models.course import Course
from Models.week import Week
from sqlalchemy import ForeignKey


class BasicRating(db.Model):
    __tablename__ = "basic_ratings"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    course_id = db.Column(db.Integer, ForeignKey(
        "courses.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.DateTime)

    def __init__(self, rating: int, course_id: int, date: datetime):
        self.rating = rating
        self.course_id = course_id
        self.date = date

    @staticmethod
    def create(rating: int, room: str, date: datetime):
        course_id = BasicRating.get_course_id(date, room)
        if course_id:
            if BasicRating.insert(rating, course_id, date):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def insert(rating: int, course_id: int, date: datetime):
        try:
            new_rating = BasicRating(rating, course_id, date)
            db.session.add(new_rating)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_course_id(date: datetime, room: str):
        week_type = 0
        week = Week.query.filter(Week.start < date).filter(
            Week.end > date).first()
        if week.id % 2 == 0:
            week_type = 2
        else:
            week_type = 1
        weekday = date.weekday()+1
        time = date.time()
        course = Course.query.filter((Course.week_type == week_type) | (Course.week_type == 0)).filter(
            Course.day == weekday).filter(Course.start < time).filter(Course.end > time).filter(Course.room == room).first()
        if course:
            return course.id

    @staticmethod
    def mean_per_day(start: datetime, end: datetime, course_id: int):
        delta = timedelta(days=1)
        data = []
        while start <= end:
            value = 0
            mean_rating = 0
            ratings_list = BasicRating.retrieve_ratings(
                start, start+delta, course_id)
            for rating in ratings_list:
                value += rating['rating']
                mean_rating = value/len(ratings_list)
            if mean_rating != 0:
                data.append({"mean_rating": round(
                    mean_rating, 2), "date": start})
            start += delta
        return data

    @staticmethod
    def total_mean(course_id: int):
        ratings_list = BasicRating.retrieve_ratings(
            "01/01/2022", datetime.today(), course_id)
        value = 0
        for rating in ratings_list:
            value += rating['rating']
        return round(value/len(ratings_list), 2)

    @staticmethod
    def retrieve_ratings(start: datetime, end: datetime, course_id: int):
        ratings = BasicRating.query.filter(BasicRating.course_id == course_id).filter(
            BasicRating.date.between(start, end))
        ratings_schema = BasicRatingSchema(many=True)
        ratings_list = ratings_schema.dump(ratings)
        return ratings_list


class BasicRatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BasicRating
