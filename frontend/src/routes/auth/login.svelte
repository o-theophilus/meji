<script>
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Forgot from './forgot.svelte';
	import Signup from './signup.svelte';
	import Info from '$lib/info.svelte';
	import Button from '$lib/button.svelte';
	import ShowPassword from '$lib/button.show_password.svelte';
	import IG from '$lib/input_group.svelte';
	import Email from './confirm_email_template.svelte';

	let email_template;

	let form = {};
	let error = {};
	let show_password = false;

	if ($module.email) {
		form.email = $module.email;
	}

	let message = 'Get access to your Cart, Saved Items, Orders, Wishlist and Recommendations.';
	let return_url = '/';

	if ($module.message) {
		message = $module.message;
	}
	if ($module.return_url) {
		return_url = $module.return_url;
	}
	if ($module?.email) {
		form.email = $module.email;
	}

	const validate = async () => {
		error = {};
		if (!form.email) {
			error.email = 'This field is required';
		}
		if (!form.password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/login`, {
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
			$token = resp.token;
			document.location = return_url;
		} else if (resp.error == 'not confirmed') {
			$module = {
				module: Info,
				status: 200,
				title: 'Confirmation Email Sent',
				message: `Your email has not been confirmed. A confirmation message has been sent to your email: ${form.email}.`,
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
		<b>Login to your account</b>
		{@html message}
	</svelte:fragment>

	<IG name="email" {error} bind:value={form.email} type="email" placeholder="Email here" />

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
		Login
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
	Forgot password?
	<Button
		class="link"
		on:click={() => {
			$module = {
				module: Forgot,
				email: form.email
			};
		}}
	>
		Recover
	</Button>
</Form>

<div bind:this={email_template} style="display: none;">
	<Email />
</div>

<style>
</style>
