<template>
	<div :class="appClass">
		<AppHeader />
		<div class="layout-content">
			<div class="layout-content-container">
				<slot />
			</div>
		</div>
		<AppFooter />
	</div>
</template>
<script>
import AppHeader from "~/layouts/AppHeader.vue";
import AppFooter from "~/layouts/AppFooter.vue";

export default {
	name: "DefaultLayout",
	setup() {
		return {
			appClass: [
				"layout-wrapper",
				"layout-light",
			]
		};
	},
	components: {
		AppFooter,
		AppHeader
	}
}
</script>
