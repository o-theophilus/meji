<script>
	import { module } from '$lib/store.js';

	import Form from '$lib/module/form.svelte';
	import Password from '$lib/comp/password_checker.svelte';
	import Button from '$lib/comp/button.svelte';

	import Login from './login.svelte';
	import Info from '$lib/module/info.svelte';

	let form = {};
	let error = {};

	export let data;

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

		if (!form.confirm) {
			error.confirm = 'This field is required';
		} else if (form.password && !error.password && form.password !== form.confirm) {
			error.confirm = 'Password and confirm password does not match';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}password_forgot/${data.token}`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(form)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$module = {
					module: Login,
					data: {
						message: 'Your password has been changed successfully.',
						email: resp.data.user.email
					}
				};
			} else if (resp.status == 201) {
				error = resp.message;
			} else {
				$module = {
					module: Info,
					data: {
						status: 'bad',
						title: `Invalid or Expired Token`,
						message: `
**Invalid or Expired Token**;
There was an error while reading the token.

Please try again repeacting the action.`,
						button: [
							{
								name: 'Ok',
								icon: 'ok'
							}
						]
					}
				};
			}
		}
	};
</script>

<svelte:head>
	<title>Reset Password | Meji</title>
</svelte:head>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Reset Password</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">Reset your password.</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
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
				bind:value={form.confirm}
				id="confirm"
				placeholder="Your password here"
			/>
			{#if error.confirm}
				<p class="error">
					{error.confirm}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" />
		</div>
	</form>
</Form>
