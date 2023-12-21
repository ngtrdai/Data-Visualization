import {useAuthStore} from "~/stores/useAuthStore";
import {useNuxtApp} from "#app";
import {useLoadingStore} from "~/stores/useLoadingStore";

export default defineNuxtPlugin({
    name: 'userPlugin',
    async setup (nuxtApp) {
        const loading = useLoadingStore();
        loading.startLoading();
        const authStore = useAuthStore();
        authStore.fetchUser().then(() => {
            loading.stopLoading();
        }).catch(() => {
            loading.stopLoading();
        });
    },
    hooks: {
        'app:created'() {
            const nuxtApp = useNuxtApp();
        }
    }
})