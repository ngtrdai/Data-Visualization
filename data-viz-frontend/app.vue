<template>
	<NuxtLayout name="default">
		<NuxtPage />
	</NuxtLayout>
</template>
<script>
import {mapState} from "pinia";
import {useLoadingStore} from "~/stores/useLoadingStore.ts";

export default {
	name: "App",
	computed: {
		...mapState(useLoadingStore, {
			isLoading: state => state.isLoading
		})
	}
}
</script>