<script>
	import { goto } from '$app/navigation';
	import { user, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from './form.svelte';
	import Password from '$lib/comp/password_checker.svelte';
	import Button from '$lib/comp/button.svelte';
	import Login from './login.svelte';
	import Info from './info.svelte';

	import Email from './signup_email_template.svelte';
	let email;

	let form = {};
	let error = {};

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

		if (!form.confirm) {
			error.confirm = 'This field is required';
		} else if (form.password && form.password !== form.confirm && !error.password) {
			error.confirm = 'Password and confirm password does not match';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.mail_content = email.innerHTML;

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}user`, {
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
				goto('/');
				$module = {
					module: Info,
					data: {
						status: 'good',
						title: 'Confirmation Email Sent',
						message: `A confirmation message has been sent to your email`,
						button: [
							{
								name: 'Ok',
								icon: 'ok'
							}
						]
					}
				};
			} else if (resp.status == 201) {
				error = resp.message;
			} else {
				error.base = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Signup to this site</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">
		<p>This is the 'Signup' page. There's not much here.</p>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		{#if error.base}
			<p class="error">
				{error.base}
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
			<Button class="primary" name="Signup" />
		</div>
		<div class="inputGroup">
			<p>
				Already have an account? <span
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
	<Email mane={$user.name} />
</div>
