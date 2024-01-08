<template>
	<div>
		Test
	</div>
</template>
<script>
import AppHeader from "~/layouts/app-header.vue";

export default {
	setup() {
		definePageMeta({
			middleware: ["auth"]
		});

		return {
			appClass: ["layout-wrapper"]
		};
	},
	components: {
		AppHeader
	}
}
</script>