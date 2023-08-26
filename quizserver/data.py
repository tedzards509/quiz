from random import randint
from typing import Dict, List
from uuid import UUID, uuid4


class LobbyData:
    def __init__(self, name, admin_uuid):
        self.name = name
        self.code = new_lobby_code()
        self.admin_ids: List[str] = [admin_uuid]
        self.user_ids: Dict[str, str] = {}  # UUID: Display Name

    def add_user(self, name) -> str:
        """
        Adds a user to the lobby.
        :param name: The display name of the user.
        :return: The UUID of the user.
        """
        uuid = str(uuid4())
        self.user_ids[uuid] = name
        return uuid


def new_lobby_code() -> str:
    while True:
        code = str(randint(10000, 99999))
        if code not in lobbies:
            return code


def generate_lobby(name: str) -> (LobbyData, str, str):
    lobby_id = str(uuid4())
    admin_id = str(uuid4())
    new_lobby = LobbyData(name, admin_id)
    lobbies[lobby_id] = new_lobby
    code_to_lobby[lobbies[lobby_id].code] = lobby_id
    return new_lobby, admin_id, lobby_id


lobbies: Dict[str, LobbyData] = {}  # lobby_id: LobbyData
code_to_lobby: Dict[str, str] = {}  # code: lobby_id

passphrase = 'Sehr gutes Passwort 123!'


def seed_data():  # TODO Remove testing data
    test_lobby = LobbyData('Test', 'admin')
    test_lobby.code = '12345'
    test_lobby.user_ids['0b2b5723-21ad-4004-9c54-bac298436243'] = 'Test Zards'
    lobbies['20333dda-3a01-4ead-b8bc-6394f292ed59'] = test_lobby
    code_to_lobby[test_lobby.code] = '20333dda-3a01-4ead-b8bc-6394f292ed59'
    print('Seeded data')
