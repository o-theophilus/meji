<script>
	import { module } from '$lib/store.js';

	import Form from '$lib/module/form.svelte';
	import Login from './login.svelte';
	import Info from '$lib/module/info.svelte';
	import Signup from './signup.svelte';
	import Button from '$lib/button.svelte';

	import Email from './forgot_email_template.svelte';
	let email_template;

	let form = {};
	let error = {};

	if ($module.email) {
		form.email = $module.email;
	}

	const validate = async () => {
		error = {};

		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'Please enter a valid email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot_password`, {
			method: 'post',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(form)
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$module = {
				module: Info,
				status: 200,
				title: 'Password Recovery Email Sent',
				message: `A password recovery message has been sent to your email`,
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
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
		<div class="title">Forgot Password</div>
	</svelte:fragment>

	<svelte:fragment slot="info">
		Please enter your email below to send a password reset link to your email.
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="email"> Email: </label>
			<input type="email" bind:value={form.email} id="email" placeholder="Your email here" />
			{#if error.email}
				<p class="error">
					{error.email}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button
				class="primary"
				name="Send"
				on:click={() => {
					validate();
				}}
			/>
		</div>

		<div class="inputGroup">
			<p>
				Don't have an account?
				<Button
					class="link"
					name="Signup"
					on:click={() => {
						$module = {
							module: Signup,
							email: form.email
						};
					}}
				/>
			</p>
		</div>
		<div class="inputGroup">
			<p>
				Remember your password?
				<Button
					class="link"
					name="Login"
					on:click={() => {
						$module = {
							module: Login,
							email: form.email
						};
					}}
				/>
			</p>
		</div>
	</form>
</Form>

<div bind:this={email_template} style="display: none;">
	<Email />
</div>
