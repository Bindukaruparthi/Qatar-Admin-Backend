from flask import Blueprint, request, jsonify
from models import db, Opportunity
from flask_jwt_extended import jwt_required, get_jwt_identity

opp_bp = Blueprint("opportunities", __name__)

@opp_bp.route("/test", methods=["GET"])
def test():
    print("TEST API HIT")
    return {"message": "Test working"}

# Get all opportunities for the logged in admin
@opp_bp.route("/", methods=["GET"])
@jwt_required()
def get_opportunities():
    
    print("CREATE API CALLED")
    print(request.json)
    
    admin_id = get_jwt_identity()

    data = Opportunity.query.filter_by(admin_id=admin_id).all()

    return jsonify([{
        "id": o.id,
        "name": o.name,
        "category": o.category,
        "duration": o.duration,
        "start_date": o.start_date,
        "description": o.description
    } for o in data])

## Create a new opportunity for the logged in admin
@opp_bp.route("/", methods=["POST"])
@jwt_required()
def create_opportunity():
    admin_id = get_jwt_identity()
    data = request.json

    opp = Opportunity(
        admin_id=admin_id,
        name=data["name"],
        duration=data["duration"],
        start_date=data["start_date"],
        description=data["description"],
        skills=data["skills"],
        category=data["category"],
        future_opportunities=data["future_opportunities"],
        max_applicants=data.get("max_applicants")
    )

@opp_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_one(id):
    admin_id = get_jwt_identity()
    opp = Opportunity.query.get(id)

    if not opp or str(opp.admin_id) != str(admin_id):
        return {"error": "Not found"}, 404

    return {
        "id": opp.id,
        "name": opp.name,
        "category": opp.category,
        "duration": opp.duration,
        "start_date": opp.start_date,
        "description": opp.description,
        "skills": opp.skills,
        "future_opportunities": opp.future_opportunities,
        "max_applicants": opp.max_applicants
    }
    
@opp_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_opportunity(id):
    print("PUT API CALLED")   # debug

    admin_id = get_jwt_identity()
    opp = Opportunity.query.get(id)

    if not opp or str(opp.admin_id) != str(admin_id):
        return {"error": "Unauthorized"}, 403

    data = request.json

    for key in data:
        setattr(opp, key, data[key])

    db.session.commit()

    return {"message": "Updated"}, 200

@opp_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_opportunity(id):
    print("DELETE API CALLED")  # debug

    admin_id = get_jwt_identity()
    opp = Opportunity.query.get(id)

    if not opp or str(opp.admin_id) != str(admin_id):
        return {"error": "Unauthorized"}, 403

    db.session.delete(opp)
    db.session.commit()

    return {"message": "Deleted"}, 200
    db.session.add(opp)
    db.session.commit()

    return jsonify({"message": "Created"}), 201