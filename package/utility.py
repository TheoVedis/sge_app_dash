import dash

# TODO fusionner les input et les states
def dash_kwarg(outputs, inputs, states):
    """Documentation
    S'applique apres un callback pour donner plusieur parametre a la fonction.
    Ordonne les parametres sous forme de dictionnaire.

    Parametre:
        outputs: les sorties d'un callback
        inputs: les entrées d'un callback
        states: les states d'un callback (entrées non declenchante)
    """

    def accept_func(func):
        def wrapper(*args):
            ctx: dash._callback_context.CallbackContext = dash.callback_context

            if len(ctx.triggered) > 1:
                print("context callback > 1 ? POSSIBLE ?!")

            if ctx:
                trigger = {
                    "id": ctx.triggered[0]["prop_id"],
                    "value": ctx.triggered[0]["value"],
                }
            else:
                trigger = (None, None)
                print("ERROR ?")

            out_dict = {}
            for item in outputs:
                try:
                    out_dict[item.component_id][
                        item.component_property
                    ] = dash.no_update
                except KeyError:
                    out_dict[item.component_id] = {
                        item.component_property: dash.no_update
                    }

            ind = 0
            input_dict = {}
            for item in inputs:
                try:
                    input_dict[item.component_id][item.component_property] = args[ind]
                except KeyError:
                    input_dict[item.component_id] = {item.component_property: args[ind]}
                ind += 1

            for item in states:
                try:
                    input_dict[item.component_id][item.component_property] = args[ind]
                except KeyError:
                    input_dict[item.component_id] = {item.component_property: args[ind]}
                ind += 1

            # print(out_dict)
            # print(input_dict)
            # print(state_dict)

            kwargs_dict = {
                "outputs": out_dict,
                "inputs": input_dict,
                "trigger": trigger,
            }
            return dash_return(func(**kwargs_dict))

        return wrapper

    return accept_func


def dash_return(outputs: dict):
    """Documentation
    Mise en forme des sorties pour correspondre aux attentes de Dash

    Parametre:
        outputs: Dictionnaires des sorties

    Sortie:
        listes des sorties et de leur valeur
    """
    out = []
    for component_id in outputs:
        for component_property in outputs[component_id]:
            out.append(outputs[component_id][component_property])

    return out