import Keycloak from "keycloak-js";

export default defineNuxtPlugin(((app) => {
    const runtimeConfig = useRuntimeConfig();
    const keycloak = new Keycloak({
        realm: runtimeConfig.public.keycloakRealm,
        url: runtimeConfig.public.keycloakUrl,
        clientId: runtimeConfig.public.keycloakClientId,
    });

    keycloak.init({
        onLoad: "login-required",
    }).then((auth) => {
        if (!auth) {
            window.location.reload();
        } else {
            console.log("Authenticated");
        }
    }).catch(() => {
        console.error("Authenticated Failed");
    });

    keycloak.updateToken(2000).then(r => {
        console.log(r);
    });

    app.$keycloak = keycloak;
}))