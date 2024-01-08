export default defineNuxtConfig({
    modules: [
        "nuxt-primevue",
        "@pinia/nuxt"
    ],
    devtools: { enabled: true },
    primevue: {
        usePrimeVue: true,
        cssLayerOrder: 'primevue, tailwind-base, tailwind-utilities',
        components: {
            include: '*'
        }
    },
    pinia: {
        storesDirs: [
            '~/stores'
        ],
    },
    app: {
        baseURL: '/',
        head: {
            title: 'DATAVIZ',
            meta: [
                { charset: 'utf-8' },
                { name: 'viewport', content: 'width=device-width, initial-scale=1' },
                { name: 'description', content: 'Data Visualization' }
            ]
        },
    },
    runtimeConfig: {
        public: {
            apiUrl: process.env.API_URL,
            appUrl: process.env.APP_URL,
            keycloakUrl: process.env.KEYCLOAK_URL,
            keycloakRealm: process.env.KEYCLOAK_REALM,
            keycloakClientId: process.env.KEYCLOAK_CLIENT_ID,
        }
    },
    css: [
        "primeflex/primeflex.css",
        "primeicons/primeicons.css",
        "primevue/resources/themes/lara-light-green/theme.css",
        "@/assets/styles/layout/layout.scss"
    ]
})