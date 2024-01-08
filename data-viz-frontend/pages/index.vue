<template>
	<div>
		<strong>Welcome back, {{ userProfile.name }} 🚀</strong>
	</div>
</template>
<script>
import {mapState} from "pinia";
import {useAuthStore} from "~/stores/useAuthStore.js";

export default {
	name: "Home",
	computed: {
		...mapState(useAuthStore, {
			userProfile: state => state.userProfile
		})
	}
}
</script>