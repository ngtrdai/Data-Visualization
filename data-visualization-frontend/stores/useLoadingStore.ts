export const useLoadingStore = defineStore('loading', () => {
    const isLoading = ref(false);
    const startLoading = () => isLoading.value = true;
    const stopLoading = () => isLoading.value = false;
    return {
        isLoading,
        startLoading,
        stopLoading
    };
});