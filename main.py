from types import prepare_class
from typing import Dict
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dash import Dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_html_components.Data import Data

from package import login_manager as lm
from package.utility import dash_kwarg

external_stylesheets = ["/assets/css/bWLwgP.css", "/assets/css/stylesheets.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


layout_login = html.Div(
    id="login_form",
    className="login",
    children=[
        html.Div(className="container"),
        html.H2(className="msg", children="Entrez vos identifiants de connexion."),
        dcc.Input(
            id="login_username",
            type="text",
            placeholder="Entrer un nom d'utilisateur",
            name="uname",
            required=False,
        ),
        dcc.Input(
            id="login_password",
            type="password",
            placeholder="Mot de passe",
            name="psw",
            required=False,
        ),
        html.H5(id="login_retour"),
        html.Button(
            id="login_button",
            n_clicks=0,
            type="submit",
            children="SE CONNECTER",
        ),
    ],
)

layout_main = html.Div("Hello")

# Pour eviter les erreur du type "input inexistante" mettre tout les layout de toutes les page dans le head
# même si elles seront écrasé par la suite
head = html.Div(
    children=[
        # Represente l'url
        dcc.Location(id="url", refresh=False),
        # Represente le stockage de variable de session
        dcc.Store(id="session", storage_type="session"),
        # Banniere
        html.Div(
            children=[html.H2("SGE_APP"), html.Img(src="/assets/img/stock-icon.png")],
            className="banner",
        ),
        html.Div(id="page-content", hidden=True, children=[layout_login, layout_main]),
    ]
)

# Affichage par defaut
app.layout = head

# Layout complet - Utilité ?!
# app.validation_layout = html.Div([head, layout_login, layout_main])

# Ensemble des outputs pour le callback ci-dessous
outputs = [
    Output("page-content", "hidden"),
    Output("page-content", "children"),
    Output("url", "pathname"),
    Output("session", "data"),
    Output("login_retour", "children"),
    Output("login_username", "required"),
    Output("login_password", "required"),
]
# Ensemble des inputs pour le callback ci-dessous
inputs = [
    Input("url", "pathname"),
    Input("login_button", "n_clicks"),
]
# Ensemble des states pour le callback ci-dessous
states = [
    State("login_username", "value"),
    State("login_password", "value"),
    State("session", "data"),
]


@app.callback(outputs, inputs, states)
@dash_kwarg(outputs, inputs, states)
def rooter(outputs: Dict[str, Dict], inputs: Dict[str, Dict], trigger: Dict):
    """Documentation
    Gestion des différents déclencheur (trigger) et sortie

    Parametre:
        outputs: Dictionnaire des variables de sortie initialisé a la valeur dash.no_update
            format ouputs[component_id][component_property]
        inputs: Dictionnaire des variables d'entrée (déclencheur (trigger) et les statiques (states)) avec leur valeur
            format inputs[component_id][component_property]
        trigger: Dictionnaire du composant déclencheur
            trigger["id"] => component_id.component_property ex: "url.pathname"
            trigger["value"] => valeur du composant ex: '/login'

    Sortie:
        outputs: Avec des variables changées ou des dash.no_update
    """

    print("Trigger :", trigger)

    # cas changement d'url ou acces au site
    if trigger["id"] == "url.pathname":
        outputs["page-content"]["children"], outputs["url"]["pathname"] = display_page(
            inputs["session"]["data"]
        )
        outputs["page-content"]["hidden"] = False

    # Cas click sur le bouton login
    if trigger["id"] == "login_button.n_clicks":
        (
            outputs["session"]["data"],
            outputs["login_retour"]["children"],
            outputs["login_username"]["required"],
            outputs["login_password"]["required"],
        ) = login(
            inputs["login_button"]["n_clicks"],
            inputs["login_username"]["value"],
            inputs["login_password"]["value"],
            inputs["session"]["data"],
        )

        # Si l'utilisateur a réussi a se connecter
        if outputs["session"]["data"]["is_logged"]:
            (
                outputs["page-content"]["children"],
                outputs["url"]["pathname"],
            ) = display_page(inputs["session"]["data"])

        outputs["page-content"]["hidden"] = False

    return outputs


def display_page(data: Dict[str, Dict]):
    """Documentation
    Gestion de l'affichage des différentes pages de l'application

    Parametre:
        data: dictionnaire composée des variables de session de l'utilisateur

    Sortie:
        output["page-content"]["children"]: Le layout contenant la structure de la page a afficher
        output["url"]["pathname"]: L'adresse de la page (chemin sur le site)

    """
    data = data or {}
    if not lm.is_logged(data):
        return layout_login, "./login"
    return layout_main, "./"


def login(n_clicks, username, password, data):
    """Documentation
    Gere les connexions au site et l'affiche d'un code d'erreur.

    Parametre:
        n_clicks: nombre de click sur le bouton "se connecter"
        username: valeur dans le champ "nom d'utilisateur"
        password: valeur dans le champ "mot de passe"
        data: dictionnaire composée des variables de session de l'utilisateur

    Sortie:
        outputs["session"]["data"]: dictionnaire des variables de session de l'utilisateur
        outputs["login_retour"]["children"]: Champ de retour pour afficher le message erreur
        outputs["login_username"]["required"]: True le champ "nom d'utilisateur" s'affiche en rouge
        outputs["login_password"]["required"]: True le champ "mot de passe" s'affiche en rouge
    """
    data = data or {}
    if n_clicks == 0:
        raise PreventUpdate

    username = username or ""
    password = password or ""

    print("ID :", username, "/", password)

    # Affichage des champs en rouge
    if len(username) == 0 or len(password) == 0:
        data["is_logged"] = False
        return (
            data,
            dash.no_update,
            len(username) == 0,
            len(password) == 0,
        )

    # Verification du couple (username, password)
    val = lm.check_password(username, password)

    # Couple valide
    if val == 0:
        data["is_logged"] = True
        data["username"] = username
        data["n_try"] = 0
        # data["type"] = "SGE" # ou autre en fct de l'username?
        pathname = "./"
        return data, "connexion reussie !", dash.no_update, dash.no_update

    # Mot de passe incorrect
    elif val == 1:
        data["is_logged"] = False
        try:
            data["n_try"] += 1
        except KeyError:
            data["n_try"] = 1

        return (
            data,
            "mot de passe incorrect",
            dash.no_update,
            dash.no_update,
        )

    # Nom d'utilisateur incorrect
    elif val == 2:
        data["is_logged"] = False
        try:
            data["n_try"] += 1
        except KeyError:
            data["n_try"] = 1

        return (
            data,
            "nom d'utilisateur incorrect",
            dash.no_update,
            dash.no_update,
        )

    # Cas jamais atteint
    print("ERROR LOGIN")
    raise PreventUpdate


app.run_server(debug=True)
