<template>
	<div
		aria-haspopup="true"
		aria-controls="actions-menu"
		@click="toggleMenuAction"
		class="flex align-items-center h-2rem px-2 transition-all transition-duration-300 hover:text-white cursor-pointer"
	>
		<i class="pi pi-fw pi-plus" style="color: var(--primary-color);"/>
		<span class="ml-1 pi pi-angle-down text-600"></span>
	</div>
	<TieredMenu ref="menuAction"
				:model="menuActions"
				id="actions-menu"
				:popup="true"
				class="w-full md:w-15rem mt-1"
				:style="{zIndex: 2000}" />
</template>
<script>
export default {
	name: "MenuAction",
	data() {
		return {
			menuActions: [
				{
					label: "Data",
					icon: "pi pi-fw pi-database",
					items: [
						{
							label: "Create dataset",
							command: () => {
								console.log("Create dataset");
							}
						},
						{
							label: "Connect Google Sheet",
							command: () => {
								console.log("Add New Widget");
							}
						}
					]
				},
				{
					label: "SQL Query",
					icon: "pi pi-fw pi-search",
					command: () => {
						console.log("SQL Query");
					}
				},
				{
					label: "Chart",
					icon: "pi pi-fw pi-chart-bar",
					command: () => {
						console.log("Chart");
					}
				},
				{
					label: "Dashboard",
					icon: "pi pi-fw pi-th-large",
					command: () => {
						console.log("Dashboard");
					}
				}
			]
		}
	},
	methods: {
		toggleMenuAction(event) {
			this.$refs.menuAction.toggle(event);
		}
	}
}
</script>