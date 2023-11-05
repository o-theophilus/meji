<script>
	import { goto } from '$app/navigation';
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Password from './password_checker.svelte';
	import Button from '$lib/button.svelte';
	import ShowPassword from '$lib/button.show_password.svelte';
	import Login from './login.svelte';
	import Info from '$lib/info.svelte';
	import IG from '$lib/input_group.svelte';
	import Email from './confirm_email_template.svelte';
	let email_template;

	let form = {};
	let error = {};
	let show_password = false;

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

		$loading = "loading . . .";
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
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
		<b> Signup to this site </b>
		This is the 'Signup' page. There's not much here.
	</svelte:fragment>

	<IG name="name" label="Fullname" {error} let:id>
		<input bind:value={form.name} {id} type="text" placeholder="Fullname here" />
	</IG>

	<IG name="email" {error} let:id>
		<input bind:value={form.email} {id} type="email" placeholder="Email here" />
	</IG>

	<IG name="password" {error} let:id>
		<div class="password">
			{#if show_password}
				<input bind:value={form.password} {id} type="text" placeholder="Password here" />
			{:else}
				<input bind:value={form.password} {id} type="password" placeholder="Password here" />
			{/if}
			<ShowPassword bind:show_password />
		</div>
		<Password password={form.password} />
	</IG>

	<IG name="confirm password" {error} let:id>
		{#if show_password}
			<input bind:value={form.confirm_password} {id} type="text" placeholder="Password here" />
		{:else}
			<input bind:value={form.confirm_password} {id} type="password" placeholder="Password here" />
		{/if}
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
		Signup
	</Button>

	<br />
	Already have an account?
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

<style>
	.password {
		position: relative;
	}
</style>
