// alert("If you see this alert, then your custom JavaScript script has run!");

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        openNav: function (val) {
            if (val == undefined) {
                return window.dash_clientside.no_update;
            }
            if (val % 2 == 0) {
                document.getElementById("sideMenu").style.width = "350px";
                document.getElementById("page-content").style.marginLeft =
                    "350px";
                return window.dash_clientside.no_update;
            } else {
                document.getElementById("sideMenu").style.width = "0px";
                document.getElementById("page-content").style.marginLeft =
                    "0px";
                return window.dash_clientside.no_update;
            }
        },
    },
});
