<template>
	<Menubar :model="items" />
</template>
<script>
export default {
	name: 'MenuMain',
	data() {
		return {
			items: [
				{
					label: 'Home',
				},
				{
					label: 'Dashboards',
				},
				{
					label: 'Charts',
				},
				{
					label: 'Datasets',
				},
				{
					label: 'SQL',
					items: [
						{
							label: 'SQL Lab'
						},
						{
							label: 'Saved Queries'
						},
						{
							label: 'Queries History'
						}
					]
				}
			]
		};
	}
}
</script>
<style scoped>
.p-menubar {
	padding: 0;
	background: none;
	border: none;
	border-radius: 0;
}
</style>