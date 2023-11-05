<script>
	import { module, loading } from '$lib/store.js';

	import Form from '$lib/form.svelte';
	import Login from './login.svelte';
	import Info from '$lib/info.svelte';
	import Signup from './signup.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
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

		$loading = "sending . . .";
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot_password`, {
			method: 'post',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

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
		<b>Forgot Password</b>
		Please enter your email below to send a password reset link to your email.
	</svelte:fragment>

	<IG name="email" {error} let:id>
		<input bind:value={form.email} {id} type="email" placeholder="Your email here" />
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button
		class="primary"
		on:click={() => {
			validate();
		}}
	>
		Send
	</Button>

	<br />
	Don't have an account?
	<Button
		class="link"
		on:click={() => {
			$module = {
				module: Signup,
				email: form.email
			};
		}}
	>
		Signup
	</Button>

	<br />
	Remember your password?
	<Button
		class="link"
		on:click={() => {
			$module = {
				module: Login,
				email: form.email
			};
		}}
	>
		Login
	</Button>
</Form>

<div bind:this={email_template} style="display: none;">
	<Email />
</div>
