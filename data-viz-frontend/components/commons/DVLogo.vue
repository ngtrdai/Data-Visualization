<template>
	<div class="layout-header-logo__container">
		<nuxt-link to="/" class="layout-header-logo" aria-label="Data Visualization">
			<div class="layout-header-logo__text">
				<span class="layout-header-logo__text--data">Data</span>
				<span class="layout-header-logo__text--viz">Viz</span>
			</div>
		</nuxt-link>
		<nuxt-link to="/" class="layout-header-icon" aria-label="Data Visualization">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="layout-header-icon__svg">
				<path d="M0 0h24v24H0z" fill="none" />
				<path
					d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm-1 15.5v-11l6 5.5-6 5.5z"
				/>
			</svg>
		</nuxt-link>
	</div>
</template>
<script>
export default {
	name: "DVLogo"
}
</script>