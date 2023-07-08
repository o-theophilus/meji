<script>
	import { module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Forgot from './forgot.svelte';
	import Signup from './signup.svelte';
	import Info from '$lib/module/info.svelte';
	import Button from '$lib/comp/button.svelte';

	import Email from './confirm_email_template.svelte';
	let email_template;

	let message = 'Get access to your Cart, Saved Items, Orders, Wishlist and Recommendations.';
	let return_url = '/';

	let form = {};
	let error = {};

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

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/login`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		resp = await resp.json();

		if (resp.status == 200) {
			$token = resp.token;
			document.location = return_url;
		} else if (resp.status == 401 && resp.error == 'not confirmed') {
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
		<div class="title">Login to your account</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">
		{@html message}
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		{#if error.error}
			<p class="error error--cap">
				{error.error}
			</p>
		{/if}
		<div class="inputGroup">
			<label for="email"> Email: </label>
			<input type="text" bind:value={form.email} id="email" placeholder="Your email here" />
			{#if error.email}
				<p class="error">
					{error.email}
				</p>
			{/if}
		</div>
		<div class="inputGroup">
			<label for="password"> Password: </label>
			<input
				type="password"
				bind:value={form.password}
				id="password"
				placeholder="Your password here"
			/>
			{#if error.password}
				<p class="error">
					{error.password}
				</p>
			{/if}
		</div>
		<!-- <div class="inputGroup horizontal">
			<input type="checkbox" bind:value={form.remember} id="remember" />
			<label for="remember"> Remember Me </label>
		</div> -->

		<div class="inputGroup horizontal">
			<Button
				class="primary"
				name="Login"
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
						$module = { module: Signup };
					}}
				/>
			</p>
		</div>
		<div class="inputGroup">
			<p>
				Forgot password?
				<Button
					class="link"
					name="Recover"
					on:click={() => {
						$module = { module: Forgot };
					}}
				/>
			</p>
		</div>
	</form>
</Form>

<div bind:this={email_template} style="display: none;">
	<Email />
</div>
