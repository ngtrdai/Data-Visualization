<template>
	<div>
		Test
	</div>
</template>
<script>
import AppHeader from "~/layouts/AppHeader.vue";

export default {
	setup() {
		return {
			appClass: ["layout-wrapper"]
		};
	},
	components: {
		AppHeader
	}
}
</script>