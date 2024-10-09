from flask import Blueprint, request, jsonify
from .models import db, Usuario


api = Blueprint('api', __name__)

@api.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify ([{
        'id': usuario.id,
        'nombre': usuario.nombre if len(usuario.nombre) <= 10 else usuario.nombre[:10] + '...',
        'correo': usuario.correo,
        'edad': usuario.edad

    } for usuario in usuarios])

@api.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify ({
        'id': usuario.id,
        'nombre': usuario.nombre,
        'correo': usuario.correo,
        'edad': usuario.edad
    })

@api.route('/usuarios', methods=['POST'])
def create_user():
    data = request.json
    new_usuario = Usuario(nombre=data['nombre'], correo=data['correo'], edad=data['edad'])
    db.session.add(new_usuario)
    db.session.commit()
    return jsonify(
        {
        'id': new_usuario.id,
        'nombre': new_usuario.nombre,
        'correo': new_usuario.correo,
        'edad': new_usuario.edad
        }
    ), 201

@api.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.json
    usuario= Usuario.query.get_or_404(id)
    usuario.nombre= data['nombre']
    usuario.correo= data['correo']
    usuario.edad= data['edad']
    db.session.commit()
    return jsonify(
        {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'correo': usuario.correo,
        'edad': usuario.edad
        }
    )


@api.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario= Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return '', 204

@api.route('/usuarios/count', methods=['GET'])
def count_usuarios():
    count = Usuario.query.count()
    return jsonify ({'total_usuarios': count})


@api.route('/usuarios/search', methods=['GET'])
def search_usuarios():
    nombre = request.args.get('nombre', None)
    correo = request.args.get('correo', None)
    edad = request.args.get('edad', None)
    
    query = Usuario.query
    
    if nombre:
        query = query.filter(Usuario.nombre.like(f"%{nombre}%"))
    
    if correo:
        query = query.filter(Usuario.correo.like(f"%{correo}%"))
    
    if edad:
        query = query.filter(Usuario.edad == edad)
    
    usuarios = query.all()
    
    return jsonify([{
        'id': usuario.id,
        'nombre': usuario.nombre,
        'correo': usuario.correo,
        'edad': usuario.edad
    } for usuario in usuarios])