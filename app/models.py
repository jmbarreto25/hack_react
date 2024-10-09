from flask_sqlalchemy import SQLAlchemy 

db= SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nombre = db.Column(db.String(100), nullable= False)
    correo = db.Column(db.String(100), nullable= False)
    edad = db.Column(db.Integer, nullable= False)

    def __repr__(self):
        return f'<Usuario{self.nombre}>'