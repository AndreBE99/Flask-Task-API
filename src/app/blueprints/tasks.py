from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.task import Task
from flask_jwt_extended import jwt_required, get_jwt_identity

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def list_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(owner_id=user_id).all()
    return jsonify([t.to_dict() for t in tasks])


@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    task = Task(owner_id=user_id, title=data.get('title'), description=data.get('description'))
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)
    if task.owner_id != user_id:
        return jsonify({"msg": "Forbidden"}), 403
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify(task.to_dict())


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)
    if task.owner_id != user_id:
        return jsonify({"msg": "Forbidden"}), 403
    db.session.delete(task)
    db.session.commit()
    return '', 204