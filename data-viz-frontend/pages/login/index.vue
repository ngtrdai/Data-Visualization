<template>
	<div class="dv-login-wrapper">
		<div class="login-box">
			<div class="login-box__heading">
				<h1 class="login-box__heading--title">Sign In</h1>
			</div>
			<div class="login-box__body">
				<form @submit.prevent="obSubmit">
					<div class="mb-2">
						<span>Enter your credentials to continue</span>
					</div>
					<div class="flex flex-column gap-2">
						<InputGroup>
							<InputGroupAddon>
								<i class="pi pi-user"></i>
							</InputGroupAddon>
							<InputText placeholder="Email" v-model="form.email" />
						</InputGroup>
						<InputGroup>
							<InputGroupAddon>
								<i class="pi pi-lock"></i>
							</InputGroupAddon>
							<Password
								:inputProps="{ autocomplete: 'current_password' }"
								:feedback="false"
								placeholder="Password"
								toggleMask
								v-model="form.password" />
						</InputGroup>
						<Button type="submit" label="SIGN IN" class="mt-2" />
					</div>
				</form>
			</div>
		</div>
	</div>
</template>
<script lang="ts">
import {useAuthStore} from "~/stores/useAuthStore";
import {definePageMeta} from "#imports";
import {mapActions, mapState} from "pinia";
import {navigateTo} from "#app";

export default {
	name: "Login",
	setup() {
		definePageMeta({
			middleware: ["guest"]
		});
	},
	data() {
		return {
			form: {
				email: "",
				password: ""
			}
		}
	},
	computed: {
		...mapState(useAuthStore, {
			isLoggedIn: state => state.isLoggedIn
		})
	},
	methods: {
		...mapActions(useAuthStore, ["login"]),
		obSubmit: async function () {
			if (this.isLoggedIn) {
				return navigateTo("/");
			}
			const {error} = await this.login(this.form);

			if (!error.value) {
				navigateTo("/");
			}
		}
	}
}
</script>
<style lang="scss" scoped>
.dv-login-wrapper {
	display: flex;
	justify-content: center;
	align-items: center;
	width: 100%;
	height: 100%;

	& .login-box {
		width: 550px;
		background-color: #fff;
		border-radius: 4px;
		box-shadow: 0 1px 1px #0000000d;

		&__heading {
			padding: 15px 15px 0;
			background-color: initial;
			border-bottom: 1px solid #0000;

			&--title {
				border-bottom: 1px solid #e0e0e0;
				color: #333;
				padding-bottom: 5px;
				font-size: 1.2rem;
			}
		}

		&__body {
			padding: 20px;
		}
	}
}
</style>