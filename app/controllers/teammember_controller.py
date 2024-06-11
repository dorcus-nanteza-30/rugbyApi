from flask import Blueprint, request, jsonify
from app.models.teammember import TeamMember
from extensions import db
from app.statuscodes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

# Define Blueprint
teammember_bp = Blueprint('teammember_bp', __name__, url_prefix='/api/v1/teammembers')

# Create a new team member
@teammember_bp.route('/', methods=['POST'])
def create_team_member():
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        event_id = data.get('event_id')
        position_of_player = data.get('position_of_player')
        jersey_number_of_player = data.get('jersey_number_of_player')
        biography_of_player = data.get('biography_of_player')
        image_of_player = data.get('image_of_player')
        
        if not (user_id and event_id and position_of_player and jersey_number_of_player and biography_of_player and image_of_player):
            return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST
        
        new_team_member = TeamMember(
            user_id=user_id,
            event_id=event_id,
            position_of_player=position_of_player,
            jersey_number_of_player=jersey_number_of_player,
            biography_of_player=biography_of_player,
            image_of_player=image_of_player
        )

        db.session.add(new_team_member)
        db.session.commit()

        return jsonify({'message': 'Team member created successfully'}), HTTP_201_CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Retrieve a team member by ID
@teammember_bp.route('/<int:id>', methods=['GET'])
def get_team_member(id):
    try:
        team_member = TeamMember.query.get(id)
        if not team_member:
            return jsonify({'error': 'Team member not found'}), HTTP_404_NOT_FOUND

        return jsonify({
            'id': team_member.id,
            'user_id': team_member.user_id,
            'event_id': team_member.event_id,
            'position_of_player': team_member.position_of_player,
            'jersey_number_of_player': team_member.jersey_number_of_player,
            'biography_of_player': team_member.biography_of_player,
            'image_of_player': team_member.image_of_player,
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update a team member
@teammember_bp.route('/<int:id>', methods=['PUT'])
def update_team_member(id):
    try:
        team_member = TeamMember.query.get(id)
        if not team_member:
            return jsonify({'error': 'Team member not found'}), HTTP_404_NOT_FOUND

        data = request.get_json()
        
        team_member.user_id = data.get('user_id', team_member.user_id)
        team_member.event_id = data.get('event_id', team_member.event_id)
        team_member.position_of_player = data.get('position_of_player', team_member.position_of_player)
        team_member.jersey_number_of_player = data.get('jersey_number_of_player', team_member.jersey_number_of_player)
        team_member.biography_of_player = data.get('biography_of_player', team_member.biography_of_player)
        team_member.image_of_player = data.get('image_of_player', team_member.image_of_player)

        db.session.commit()

        return jsonify({'message': 'Team member updated successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Delete a team member
@teammember_bp.route('/<int:id>', methods=['DELETE'])
def delete_team_member(id):
    try:
        team_member = TeamMember.query.get(id)
        if not team_member:
            return jsonify({'error': 'Team member not found'}), HTTP_404_NOT_FOUND

        db.session.delete(team_member)
        db.session.commit()

        return jsonify({'message': 'Team member deleted successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
