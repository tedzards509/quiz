from flask import Blueprint, request, jsonify

import data

api_blueprint = Blueprint('api_blueprint', __name__)


# Create Lobby (Host) - POST
@api_blueprint.route('/lobby', methods=['POST'])
def create_lobby():
    """
    Create a new lobby (Host).

    Request JSON:
    {
        "passphrase": "Your Passphrase",
        "name": "Lobby Name"
    }

    Response JSON:
    {
        "lobby_id": "Unique Lobby UUID",
        "code": "Unique Lobby Code",
        "admin_id": "Unique Admin UUID"
    }
    """
    passphrase = request.get_json().get('passphrase')
    name = request.get_json().get('name')

    if passphrase != data.passphrase:
        return jsonify({'message': 'Incorrect Passphrase'}), 403
    lobby, admin_id, lobby_id = data.generate_lobby(name)

    return jsonify({'lobby_id': lobby_id,
                    'code': lobby.code,
                    'admin_id': admin_id})


# Connect to Lobby (User) - POST
@api_blueprint.route('/lobby/connect', methods=['POST'])
def connect_to_lobby():
    """
    Connect to an existing lobby (User).

    Request JSON:
    {
        "code": "Lobby Code",
        "name": "Preferred Display Name"
    }

    Response JSON:
    {
        "uuid": "Your User ID",
        "lobby_uuid": "The Lobbies ID"
    }
    """
    code = request.get_json().get('code')
    name = request.get_json().get('name')

    if data.code_to_lobby.get(code) is None:
        return jsonify({'message': 'Incorrect Code',  # TODO: Remove codes attribute from this response
                        'codes': [data.lobbies[lobby_id].code for lobby_id in data.lobbies.keys()]}), 404

    user_id = data.lobbies[data.code_to_lobby[code]].add_user(name)
    return jsonify({'uuid': user_id, 'lobby_uuid': data.code_to_lobby[code]})


# Disconnect from Lobby (User) - DELETE
@api_blueprint.route('/lobby/<string:lobby_id>/<string:user_id>', methods=['DELETE'])
def disconnect_from_lobby(lobby_id, user_id):
    """
    Disconnect from a lobby (User).

    :param lobby_id: Lobby ID
    :param user_id: User that should be removed from the lobby
    :return: Success message
    """
    if data.lobbies.get(lobby_id) is None:
        return jsonify({'message': 'Lobby does not exist'}), 404
    lobby = data.lobbies[lobby_id]
    requester_id = request
    remove_user_id = user_id
    if lobby.user_ids.get(remove_user_id) is None:
        return jsonify({'message': 'User not in lobby'}), 404
    if requester_id in lobby.admin_ids or requester_id == remove_user_id:
        lobby.user_ids.pop(remove_user_id)
        return jsonify({'message': 'User removed successfully'}), 200
    return jsonify({'message': 'Not allowed'}), 403


# Post Answer (User) - POST
@api_blueprint.route('/lobby/<string:lobby_uuid>/post-answer', methods=['POST'])
def post_answer(lobby_uuid):
    """
    Post an answer to the specified lobby (User).

    :param lobby_uuid: Unique Lobby UUID
    Request JSON:
    {
        "uuid": "Unique User UUID",
        "answer": "User's Answer"
    }

    Response JSON:
    {
        "message": "Answer posted successfully"
    }
    """
    requester_id = request.get_json().get('user-id')
    answer = request.get_json().get('answer')

    # TODO: Implement logic to post an answer to the lobby

    return jsonify({'message': 'Answer posted successfully'})


# Start Next Question (Host) - PUT
@api_blueprint.route('/lobby/<string:lobby_uuid>/start-next-question', methods=['PUT'])
def start_next_question(lobby_uuid):
    """
    Start the next question in the lobby (Host).

    :param lobby_uuid: Unique Lobby UUID
    :return: Success message
    """
    requester_uuid = request.headers.get('user-id')

    if data.lobbies.get(lobby_uuid) is None:
        return jsonify({'message': 'Lobby does not exist'}), 404
    if requester_uuid not in data.lobbies[lobby_uuid].admin_ids:
        return jsonify({'message': 'You are not the host'}), 403

    # TODO: Implement logic to start the next question in the lobby, integrate websockets... somehow

    return jsonify({'message': 'Next question started'})


@api_blueprint.route('/lobby/<string:lobby_id>', methods=['GET'])
def get_lobby(lobby_id):
    """
    Get the lobby data.

    :param lobby_id: Unique Lobby UUID
    :return: Lobby data
    """
    if data.lobbies.get(lobby_id) is None:
        return jsonify({'message': 'Lobby does not exist'}), 404
    lobby = data.lobbies[lobby_id]
    return jsonify({'name': lobby.name,
                    'code': lobby.code,
                    'admins': lobby.admin_ids,
                    'users': lobby.user_ids}), 200


@api_blueprint.route('/lobby', methods=['GET'])
def get_lobbies():
    """
    Get all lobbies with the corresponding codes.

    :return: The dictionary of codes to lobby UUIDs
    """
    return jsonify({'codes': data.code_to_lobby}), 200
