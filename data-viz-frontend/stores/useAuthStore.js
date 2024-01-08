import {userSchema} from "~/stores/schemas/authSchema.js";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        auth: null,
        userProfile: userSchema,
        roles: []
    }),
    actions: {
        setup(auth) {
            this.auth = auth;
            this.userProfile = {
                name: auth.idTokenParsed?.family_name,
                email: auth.idTokenParsed?.email,
                username: auth.idTokenParsed?.preferred_username
            };

            if (auth.realmAccess?.roles) {
                this.roles = this.roles.concat(auth.realmAccess.roles);
            }

            if (auth.resourceAccess) {
                Object.keys(auth.resourceAccess).forEach(key => {
                    if (auth.resourceAccess[key].roles) {
                        this.roles = this.roles.concat(auth.resourceAccess[key].roles);
                    }
                });
            }
        },
        hasRole(role) {
            return this.roles.includes(role);
        },
        logout() {
            this.auth.logout();
        }
    },
    getters: {
        isLoggedIn() {
            return this.auth !== null;
        }
    },
});