<template>
	<div :ref="containerRef" class="layout-header">
		<div class="layout-header-inner">
			<div class="flex align-items-center">
				<DVLogo />
				<MenuMain v-if="isLoggedIn" />
			</div>
			<ul class="flex list-none m-0 p-0 gap-2 align-items-center">
				<li class="relative">
					<MenuAction v-if="isLoggedIn" />
				</li>
				<li class="relative">
					<MenuSetting v-if="isLoggedIn" />
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
import DVLogo from "~/components/commons/data-viz-logo.vue";
import MenuSetting from "~/components/headers/menu-setting.vue";
import MenuAction from "~/components/headers/menu-action.vue";
import MenuMain from "~/components/headers/menu-main.vue";
import {mapState} from "pinia";
import {useAuthStore} from "~/stores/useAuthStore.ts";

export default {
	name: "AppHeader",
	components: {MenuMain, MenuAction, MenuSetting, DVLogo},
	container: null,
	scrollListener: null,
	computed: {
		...mapState(useAuthStore, {
			isLoggedIn: state => state.isLoggedIn
		})
	},
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