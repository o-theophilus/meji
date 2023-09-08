<script>
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Forgot from './forgot.svelte';
	import Signup from './signup.svelte';
	import Info from '$lib/info.svelte';
	import Button from '$lib/button_v2.svelte';
	import IG from '$lib/input_group.svelte';
	import Email from './confirm_email_template.svelte';

	let email_template;

	let form = {};
	let error = {};
	let show = false;

	if ($module.email) {
		form.email = $module.email;
	}

	let message = 'Get access to your Cart, Saved Items, Orders, Wishlist and Recommendations.';
	let return_url = '/';

	if ($module?.message) {
		message = $module.message;
	}
	if ($module?.return_url) {
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

		$loading = true;
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
				message: `Your email has not been confirmed. A confirmation message has been sent to your email: ${resp.user.email}.`,
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

	<IG name="email" {error} let:id>
		<input bind:value={form.email} {id} type="text" placeholder="Email here" />
	</IG>

	<IG name="password" {error} let:id>
		<div class="password">
			{#if show}
				<input bind:value={form.password} {id} type="text" placeholder="Password here" />
			{:else}
				<input bind:value={form.password} {id} type="password" placeholder="Password here" />
			{/if}
			<form class="show" on:submit|preventDefault>
				<Button
					class="tiny"
					icon={show ? 'hide_password' : 'show_password'}
					icon_size="14"
					on:click={() => {
						show = !show;
					}}
				/>
			</form>
		</div>
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button
		class="primary"
		name="Login"
		on:click={() => {
			validate();
		}}
	/>

	<br />
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
	<br />
	Forgot password?
	<Button
		class="link"
		name="Recover"
		on:click={() => {
			$module = {
				module: Forgot,
				email: form.email
			};
		}}
	/>
</Form>

<div bind:this={email_template} style="display: none;">
	<Email />
</div>

<style>
	.password {
		position: relative;
	}

	.show {
		position: absolute;
		right: var(--sp2);
		top: 0;

		display: flex;
		align-items: center;

		height: 100%;
	}
</style>
