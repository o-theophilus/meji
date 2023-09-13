<script>
	import { module, user, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';
	import Password from '../../auth/password_checker.svelte';
	import Button from '$lib/button.svelte';
	import ShowPassword from '$lib/button.show_password.svelte';

	import Email from './password_email_template.svelte';
	import Info from '$lib/info.svelte';

	let form = {};
	let error = {};
	let email_template;
	let message;
	let show_password = false;

	const request_otp = async () => {
		error = {};
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/password_otp`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();

		if (resp.status == 200) {
			message = 'emails containing the OTP has been sent to your email';
		} else {
			error = resp;
		}
	};

	const validate = async () => {
		error = {};

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
		} else if (form.password && !error.password && form.password !== form.confirm_password) {
			error.confirm_password = 'Password and confirm password does not match';
		}

		if (!form.otp) {
			error.otp = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/password`, {
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
			$module = {
				module: Info,
				status: 200,
				title: 'Password Changed',
				message: 'Your password has been changed successfully.',
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
		<b> Reset Password </b>
		Reset your password.
	</svelte:fragment>

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

	<Button class="primary" on:click={request_otp}>Request OTPs</Button>
	<br />
	{#if message}
		<div class="inputGroup">
			{message}
		</div>
		<br />
	{/if}

	<IG name="otp" label="OTP" {error} let:id>
		<input bind:value={form.otp} {id} type="text" placeholder="OTP here" />
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" on:click={validate}>Submit</Button>
</Form>

<div bind:this={email_template} style="display: none;">
	<Email name={$user.name} />
</div>

<style>
	.password {
		position: relative;
	}
</style>
