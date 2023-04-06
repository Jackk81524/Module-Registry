from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Packages_table(db.Model):
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    NAME = db.Column(db.String(255), unique=True, nullable=True)
    VERSION = db.Column(db.String(50), nullable=True)
    UPDATEDBY = db.Column(db.String(50), nullable=True)
    LAST_UPDATED = db.Column(db.DateTime, nullable=True)
    RAMPUP = db.Column(db.Float, nullable=True)
    CORRECTNESS = db.Column(db.Float, nullable=True)
    BUSFACTOR = db.Column(db.Float, nullable=True)
    RESPONSIVEMAINTAINER = db.Column(db.Float, nullable=True)
    LICENSESCORE = db.Column(db.Float, nullable=True)
    GOODPINNINGPRACTICE = db.Column(db.Float, nullable=True)
    PULLREQUEST = db.Column(db.Float, nullable=True)
    NETSCORE = db.Column(db.Float, nullable=True)

def add_package(NAME):
    new_package = Packages_table(ID=31,NAME = NAME,VERSION = "v1.1.2",NETSCORE = 1.1)
    db.session.add(new_package)
    db.session.commit()

def query_package(Query):
    Name = Query.Name.Name
    Version = Query.Version.Version
    if Version == None:
        result = db.session.query(Packages_table).filter_by(NAME = Name).all()
    else:
        result = db.session.query(Packages_table).filter_by(NAME = Name,VERSION=Version).all()
    return result
    


