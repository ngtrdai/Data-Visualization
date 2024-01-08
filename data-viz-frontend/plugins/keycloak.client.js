import Keycloak from "keycloak-js";
import {useAuthStore} from "~/stores/useAuthStore.js";

export default defineNuxtPlugin(((app) => {
    const runtimeConfig = useRuntimeConfig();
    const authStore = useAuthStore();
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
            keycloak.updateToken(5).then((refreshed) => {
                if (refreshed) {
                    console.log("Token refreshed" + refreshed);
                } else {
                    console.log('Token is still valid');
                }
            }).catch(() => {
                console.error("Failed to refresh token");
            });

            authStore.setup(keycloak);
        }
    });
}))