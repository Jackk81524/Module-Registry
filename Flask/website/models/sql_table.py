from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Packages_table(db.Model):
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(214), unique=True, nullable=True)
    version = db.Column(db.String(50), nullable=True)

def add_pacakage(name):
    new_package = Packages(ID=3,name = name,version = "v1.1.1")
    db.session.add(new_package)
    db.session.commit()


