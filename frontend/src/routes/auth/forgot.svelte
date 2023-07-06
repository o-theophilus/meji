<script>
	import { page } from '$app/stores';

	import { module } from '$lib/store.js';

	import Form from '$lib/module/form.svelte';
	import Login from './login.svelte';
	import Info from '$lib/module/info.svelte';
	import Signup from './signup.svelte';
	import MD from '$lib/comp/marked.svelte';
	import Button from '$lib/comp/button.svelte';

	import Email from './forgot_email_template.svelte';
	let email;

	let message = 'Please enter your email below to send a password reset link to your email.';

	let form = {};
	let error = '';

	const validate = async () => {
		error = '';

		if (!form.email) {
			error = 'This field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error = 'Please enter a valid email';
		}

		!error && submit();
	};

	const submit = async () => {
		form.mail_content = email.innerHTML;

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}password_forgot`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(form)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$module = {
					module: Info,
					data: {
						status: 'good',
						title: 'Password Recovery Email Sent',
						message: `A password recovery message has been sent to your email`,
						button: [
							{
								name: 'Ok',
								icon: 'ok'
							}
						]
					}
				};
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Forgot Password</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">
		<MD md={message} />
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="email"> Email: </label>
			<input type="email" bind:value={form.email} id="email" placeholder="Your email here" />
			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Send" />
		</div>

		<div class="inputGroup">
			<p>
				Don't have an account? <span
					class="link"
					on:keypress
					on:click={() => {
						$module = { module: Signup };
					}}>Signup</span
				>
			</p>
		</div>
		<div class="inputGroup">
			<p>
				Remember your password? <span
					class="link"
					on:keypress
					on:click={() => {
						$module = {
							module: Login
						};
					}}>Login</span
				>
			</p>
		</div>
	</form>
</Form>

<div bind:this={email} style="display: none;">
	<Email />
</div>
