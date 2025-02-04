# filter_routes.py
from .common_imports import *

# Routes for Categories
@filter_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_data = [{"id": category.id, "name": category.name} for category in categories]
    return jsonify(categories_data), 200

@filter_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data.get('name'))
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category created successfully!"}), 201

@filter_bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if category:
        return jsonify({"id": category.id, "name": category.name}), 200
    return jsonify({"message": "Category not found"}), 404

# Routes for Tags
@filter_bp.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    tags_data = [{"id": tag.id, "name": tag.name} for tag in tags]
    return jsonify(tags_data), 200

@filter_bp.route('/tags', methods=['POST'])
def create_tag():
    data = request.get_json()
    new_tag = Tag(name=data.get('name'))
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({"message": "Tag created successfully!"}), 201

@filter_bp.route('/tags/<int:id>', methods=['GET'])
def get_tag(id):
    tag = Tag.query.get(id)
    if tag:
        return jsonify({"id": tag.id, "name": tag.name}), 200
    return jsonify({"message": "Tag not found"}), 404