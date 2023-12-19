<template>
	<div :ref="containerRef" class="layout-header">
		<div class="layout-header-inner">
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
			<ul class="flex list-none m-0 p-0 gap-2 align-items-center">
				<li class="relative">
					<button
						:style="{ selector: '@next', enterClass: 'hidden', enterActiveClass: 'scalein', leaveToClass: 'hidden', leaveActiveClass: 'fadeout', hideOnOutsideClick: true }"
						type="button"
						style="max-width: 8rem"
						class="px-link flex align-items-center surface-card h-2rem px-2 border-1 border-solid surface-border transition-all transition-duration-300 hover:border-primary"
					>
						<span class="text-900 block white-space-nowrap overflow-hidden"> 1.0.0</span>
						<span class="ml-2 pi pi-angle-down text-600"></span>
					</button>
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
export default {
	name: "AppHeader",
	container: null,
	scrollListener: null,
	mounted() {
		this.bindScrollListener();
	},
	beforeUnmount() {
		if (this.scrollListener) {
			this.unbindScrollListener();
		}
	},
	methods: {
		bindScrollListener() {
			if (!this.scrollListener && this.container) {
				this.scrollListener = () => {
					if (window.scrollY > 0) this.container.classList.add('layout-header-sticky');
					else this.container.classList.remove('layout-header-sticky');
				};
			}

			window.addEventListener('scroll', this.scrollListener);
		},
		unbindScrollListener() {
			if (this.scrollListener) {
				window.removeEventListener('scroll', this.scrollListener);
				this.scrollListener = null;
			}
		},
		containerRef(el) {
			this.container = el;
		}
	}
}
</script>