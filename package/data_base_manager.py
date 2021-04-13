from typing import List
import pyodbc
import pandas as pd

# Param de connection
conn: pyodbc.Connection = pyodbc.connect(
    "driver={SQL Server};"
    "server=SGE-PC-107;"
    "DATABASE=Test;"
    "Trusted_Connection=yes;"
)


def get_id_cpt(client: str = None) -> List[str]:
    """Documentation
    Parametre:
        client: le nom du client, du compte connecté s'il doit être restreint

    Sortie:
        la liste des id des compteurs
    """

    data: pd.DataFrame = pd.read_sql_query(
        "select distinct Id_CPT from Test.dbo.Histo"
        # "where Nom_client = '" + client + "'", # A rajouter une fois la base client intégré
        " order by Id_CPT",
        conn,
    )

    return list(data["Id_CPT"])


if __name__ == "__main__":
    print(get_id_cpt())
