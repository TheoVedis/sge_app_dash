import dash
from dash.dash import Dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Data import Data
import dash_table
from dash.exceptions import PreventUpdate
from package import login_manager as lm

external_stylesheets = ["/assets/css/bWLwgP.css", "/assets/css/stylesheets.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
        html.Div(id="page-content"),
    ]
)

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

# Affichage par defaut
app.layout = head

# Layout complet
app.validation_layout = html.Div(children=[head, layout_login, layout_main])


@app.callback(
    [Output("page-content", "children"), Output("url", "pathname")],
    Input("url", "pathname"),
    State("session", "data"),
)
def display_page(pathname, data):
    """Documentation
    Gestion de l'affichage des différentes pages de l'application
    """
    data = data or {}
    if not lm.is_logged(data):
        return layout_login, "./login"

    return layout_main, "./"


@app.callback(
    [
        Output("session", "data"),
        Output("login_retour", "children"),
        Output("login_username", "required"),
        Output("login_password", "required"),
    ],
    Input("login_button", "n_clicks"),
    [
        State("login_username", "value"),
        State("login_password", "value"),
        State("session", "data"),
        State("url", "pathname"),
    ],
)
def login(n_clicks, username, password, data, pathname):
    """Documentation
    Parametre:
        n_clicks: nombre de click sur le bouton "se connecter", declencheur
        username: nom d'utilisateur
        password: mot de passe
        data: données de la session

    Sortie:
        data: mise a jour des données utilisteur
        msg_error: affichage de l'erreur
    """
    data = data or {}
    if n_clicks == 0:
        raise PreventUpdate

    username = username or ""
    password = password or ""

    print(username, password)
    if len(username) == 0 or len(password) == 0:
        return (
            dash.no_update,
            dash.no_update,
            len(username) == 0,
            len(password) == 0,
            dash.no_update,
        )

    val = lm.check_password(username, password)

    if val == 0:
        data["is_logged"] = True
        data["username"] = username
        data["n_try"] = 0
        # data["type"] = "SGE" # ou autre en fct de l'username?
        pathname = "./"
        return data, "connexion reussie !", dash.no_update, dash.no_update

    elif val == 1:
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

    elif val == 2:
        try:
            data["n_try"] += 1
        except:
            data["n_try"] = 1

        return (
            data,
            "nom d'utilisateur incorrect",
            dash.no_update,
            dash.no_update,
        )

    raise PreventUpdate


app.run_server(debug=True)