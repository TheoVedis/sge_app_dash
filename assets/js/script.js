// alert("If you see this alert, then your custom JavaScript script has run!");

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        openNav: function (val) {
            /* Documentation
            Cette fonction a pour but d'ouvrir et fermer le menu lattéral
            ainsi que décaler le contenu de la page principal vers la droite

            Parametre:
                val: nombre de click qu'un utilisateur a effectué sur le bouton
            */
            if (val == undefined) {
                return window.dash_clientside.no_update;
            }
            if (val % 2 == 1) {
                document.getElementById("sideMenu").style.width = "350px";
                document.getElementById("page-content").style.marginLeft =
                    "350px";
                document.getElementById("sideMenu-btn").style.transform =
                    "scaleX(-1)";
                return window.dash_clientside.no_update;
            } else {
                document.getElementById("sideMenu").style.width = "0px";
                document.getElementById("page-content").style.marginLeft =
                    "0px";
                document.getElementById("sideMenu-btn").style.transform =
                    "scaleX(1)";
                return window.dash_clientside.no_update;
            }
        },
    },
});
