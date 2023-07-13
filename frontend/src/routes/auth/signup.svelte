<script>
	import { goto } from '$app/navigation';
	import { user, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Password from '$lib/comp/password_checker.svelte';
	import Button from '$lib/button.svelte';
	import Login from './login.svelte';
	import Info from '$lib/module/info.svelte';

	import Email from './confirm_email_template.svelte';
	let email_template;

	let form = {};
	let error = {};

	if ($module.email) {
		form.email = $module.email;
	}

	const validate = async () => {
		error = {};
		if (!form.name) {
			error.name = 'This field is required';
		}

		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'Please enter a valid email';
		}

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
		} else if (form.password && form.password !== form.confirm_password && !error.password) {
			error.confirm_password = 'Password and confirm password does not match';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();

		if (resp.status == 200) {
			goto('/');
			$module = {
				module: Info,
				status: 200,
				title: 'Confirmation Email Sent',
				message: `A confirmation message has been sent to your email`,
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
		<div class="title">Signup to this site</div>
	</svelte:fragment>

	<svelte:fragment slot="info">
		<p>This is the 'Signup' page. There's not much here.</p>
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		{#if error.error}
			<p class="error">
				{error.error}
			</p>
		{/if}

		<div class="inputGroup">
			<label for="name"> Fullname: </label>
			<input type="text" bind:value={form.name} id="name" placeholder="Your fullname here" />
			{#if error.name}
				<p class="error">
					{error.name}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="email"> Email: </label>
			<input type="email" bind:value={form.email} id="email" placeholder="Your email here" />
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
				name="Signup"
				on:click={() => {
					validate();
				}}
			/>
		</div>
		<div class="inputGroup">
			<p>
				Already have an account?
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
