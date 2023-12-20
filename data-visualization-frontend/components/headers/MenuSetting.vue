<template>
	<Button
		type="button"
		aria-haspopup="true"
		aria-controls="settings-menu"
		@click="toggleMenuSetting"
		class="flex align-items-center surface-card h-2rem px-2 border-1 border-solid surface-border transition-all transition-duration-300 hover:border-primary"
	>
		<span class="text-900 block white-space-nowrap overflow-hidden">Settings</span>
		<span class="ml-2 pi pi-angle-down text-600"></span>
	</Button>
	<Menu ref="menuSetting"
		  :model="menuSettings"
		  id="settings-menu"
		  :popup="true"
		  class="w-full md:w-18rem mt-1"
		  :style="{zIndex: 2000}"
	>
		<template v-slot:start>
			<div class="p-submenu-header">
				<span class="font-medium text-xl font-semibold">DATA<span class="text-primary">VIZ</span></span>
			</div>
		</template>
		<template v-slot:submenuheader="{item}">
			<span class="text-primary font-bold">{{item.label}}</span>
		</template>
		<template v-slot:item="{item, props}">
			<a v-bind="props.action" class="flex align-items-center">
				<span :class="item.icon" />
				<span class="ml-2">{{ item.label }}</span>
			</a>
		</template>
		<template v-slot:end>
			<div class="p-submenu-header">
				<span class="text-primary font-bold">About</span>
				<div class="about-section">
					<div>Powered by LAMPSpace</div>
					<div>Version 1.0.0</div>
				</div>
			</div>
		</template>
	</Menu>
</template>
<script>

export default {
	name: "MenuSetting",
	data() {
		return {
			menuSettings: [
				{
					label: "Data",
					items: [
						{
							label: "Database Connections",
							icon: "pi pi-fw pi-database",
							command: () => {
								console.log("Data Connection");
							}
						}
					]
				},
				{
					label: "User",
					items: [
						{
							label: "Logout",
							icon: "pi pi-sign-out",
							command: () => {
								console.log("Logout");
							}
						}
					]
				}
			]
		}
	},
	methods: {
		toggleMenuSetting(event) {
			this.$refs.menuSetting.toggle(event);
		}
	}
}
</script>

<style scoped>
.about-section {
	margin-top: 0.5rem;
	font-weight: lighter;
	font-size: 10px;
}
</style>