<script>
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Password from '$lib/comp/password_checker.svelte';
	import Button from '$lib/button.svelte';

	import Info from '$lib/module/info.svelte';
	import Login from './login.svelte';
	import Forgot from './forgot.svelte';

	let form = {};
	let error = {};

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
		$loading = 'loading . . .';
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
		<div class="title">Reset Password</div>
	</svelte:fragment>

	<svelte:fragment slot="info">Reset your password.</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="password"> Password: </label>
			<input
				type="password"
				bind:value={form.password}
				id="password"
				placeholder="Your password here"
			/>
			<Password password={form.password} />

			{#if error.password}
				<p class="error">
					{error.password}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="confirm"> Confirm Password: </label>
			<input
				type="password"
				bind:value={form.confirm_password}
				id="confirm"
				placeholder="Your password here"
			/>
			{#if error.confirm_password}
				<p class="error">
					{error.confirm_password}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button
				class="primary"
				name="Submit"
				on:click={() => {
					validate();
				}}
			/>
		</div>
	</form>
</Form>
