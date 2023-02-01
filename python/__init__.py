from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma = Marshmallow()


def init_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from Models.basicRating import BasicRating
        from Models.complexRating import ComplexRating
        from Models.course import Course
        from Models.professor import Professor
        from Models.week import Week
        from Models.faculty import Faculty
        from Models.programme import Programme
        from Models.programmeCourses import ProgrammeCourses

        db.create_all()

        from routes import basic_rating_bp as basic_rating_bp
        from routes import complex_rating_bp as complex_rating_bp
        from routes import course_bp as course_bp
        from routes import professor_bp as professor_bp
        from routes import week_bp as week_bp
        from routes import faculty_bp as faculty_bp
        from routes import programme_bp as programme_bp
        from routes import prog_courses_bp as prog_courses_bp

        app.register_blueprint(basic_rating_bp)
        app.register_blueprint(complex_rating_bp)
        app.register_blueprint(course_bp)
        app.register_blueprint(professor_bp)
        app.register_blueprint(week_bp)
        app.register_blueprint(faculty_bp)
        app.register_blueprint(programme_bp)
        app.register_blueprint(prog_courses_bp)

        return app
