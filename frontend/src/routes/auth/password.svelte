<script>
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Password from './password_checker.svelte';
	import Button from '$lib/button.svelte';
	import ShowPassword from '$lib/button.show_password.svelte';
	import IG from '$lib/input_group.svelte';
	import Info from '$lib/info.svelte';
	import Login from './login.svelte';
	import Forgot from './forgot.svelte';

	let form = {};
	let error = {};
	let show_password = false;

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'This field is required';
		} else if (
			!/[a-z]/.test(form.password) ||
			!/[A-Z]/.test(form.password) ||
			!/[0-9]/.test(form.password) ||
			form.password.length < 8 ||
			form.password.length > 18
		) {
			error.password =
				'Password must include at least 1 lowercase letter, 1 uppercase letter, 1 number and must contain 8 - 18 characters';
		}

		if (!form.confirm_password) {
			error.confirm_password = 'This field is required';
		} else if (form.password && !error.password && form.password !== form.confirm_password) {
			error.confirm_password = 'Password and confirm password does not match';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'resetting . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot_password/${$module.token}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$module = {
				module: Info,
				status: 200,
				title: 'Password Changed',
				message: 'Your password has been changed successfully.',
				button: [
					{
						name: 'Login',
						icon: 'ok',
						fn: () => {
							$module = {
								module: Login,
								email: resp.user.email
							};
						}
					}
				]
			};
		} else if (resp.error == 'invalid token') {
			$module = {
				module: Info,
				status: 400,
				title: 'Invalid or Expired Token',
				message: `
**Invalid or Expired Token**;
There was an error while reading the token.

Please try repeacting the action again.`,
				button: [
					{
						name: 'Try Again',
						icon: 'ok',
						fn: () => {
							$module = {
								module: Forgot
							};
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b> Reset Password </b>
		Reset your password.
	</svelte:fragment>

	<IG
		name="password"
		{error}
		bind:value={form.password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	>
		<svelte:fragment slot="pos_1">
			<ShowPassword bind:show_password />
		</svelte:fragment>
		<svelte:fragment slot="pos_2">
			<Password password={form.password} />
		</svelte:fragment>
	</IG>

	<IG
		name="confirm password"
		{error}
		bind:value={form.confirm_password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" on:click={validate}>Reset</Button>
</Form>

<style>
</style>
