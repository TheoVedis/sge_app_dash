# Test acc
account = {"test": "mdp"}


def is_logged(data: dict) -> bool:
    """Documentation
    Verifie si un utilisateur est connecté.

    Parametre:
        data: dictionnaire des données session de l'utilisateur

    Sortie:
        True: L'utilisateur est connecté
        False: l'utilistauer n'est pas connecté
    """

    if "is_logged" not in data.keys():
        return False

    return data["is_logged"]


# TODO version BD?
def check_password(username: str, password: str) -> int:
    """Documentation
    Verifie le couple (username, password) et renvoie une valeur en fonction

    Parametre:
        username: Nom d'utilisateur
        password: Mot de passe

    Sortie:
        0: Connexion reussie
        1: Mot de passe incorrect
        2: Nom d'utilisateur inconnue
    """
    try:
        return int(account[username] != password)
    except KeyError:
        pass

    return 2


if __name__ == "__main__":
    print(check_password("test", "mdp"))