<script>
	import { user, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Forgot from './forgot.svelte';
	import Signup from './signup.svelte';
	import Info from '$lib/module/info.svelte';
	import Button from '$lib/comp/button.svelte';

	import Email from './login_email_template.svelte';
	let email;

	export let data;
	let message = 'Get access to your Cart, Saved Items, Orders, Wishlist and Recommendations.';
	let return_url = '/';

	let form = {};
	let error = {};

	if (data?.message) {
		message = data.message;
	}
	if (data?.return_url) {
		return_url = data.return_url;
	}
	if (data?.email) {
		form.email = data.email;
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
		form.mail_content = email.innerHTML;
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}login`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$token = resp.data.token;
				document.location = return_url;
			} else if (resp.status == 201 && resp.message == 'not confirmed') {
				$module = {
					module: Info,
					data: {
						status: 'good',
						title: 'Confirmation Email Sent',
						message: `Your email has not been confirmed. A confirmation message has been sent to your email: ${resp.data.user.email}.`,
						button: [
							{
								name: 'Ok',
								icon: 'ok'
							}
						]
					}
				};
			} else {
				error.form = resp.message;
			}
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

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		{#if error.form}
			<p class="error error--cap">
				{error.form}
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
			<Button class="primary" name="Login" />
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
				Forgot password? <span
					class="link"
					on:keypress
					on:click={() => {
						$module = { module: Forgot };
					}}>Recover</span
				>
			</p>
		</div>
	</form>
</Form>

<div bind:this={email} style="display: none;">
	<!-- <Email /> -->
</div>
