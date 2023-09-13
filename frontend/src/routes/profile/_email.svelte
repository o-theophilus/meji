<script>
	import { module, portal, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Email from './email_email_template.svelte';

	let form = {};
	let error = {};
	let email_template;
	let message = '';
	let user = { ...$module.user };

	const validate_request_otp = () => {
		error = {};
		message = '';

		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'please enter a valid email';
		} else if (form.email == user.email) {
			error.email = 'please use a different email form your current email';
		}

		Object.keys(error).length === 0 && request_otp();
	};

	const request_otp = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/email_otp`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();

		if (resp.status == 200) {
			message = 'emails containing the OTP has been sent to your current email and your new email';
		} else {
			error = resp;
		}
	};

	const validate = () => {
		error = {};
		message = '';

		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'Please enter a valid email';
		}

		if (!form.otp_1) {
			error.otp_1 = 'This field is required';
		}

		if (!form.otp_2) {
			error.otp_2 = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/email`, {
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
			$portal = resp.user;
			$module = '';
			$toast = {
				status: 200,
				message: 'Email changed'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Change Email</b>
		Change your account Email.
	</svelte:fragment>

	<span class="f1">Current Email: {user.email}</span>

	<br />
	<br />

	<IG name="email" label="New Email" {error} let:id>
		<input type="email" bind:value={form.email} id="email" placeholder="your new email here" />
	</IG>

	<Button class="primary" on:click={validate_request_otp}>Request OTPs</Button>
	{#if message}
		<br />
		<span class="f1">
			{message}
		</span>
		<br />
	{/if}
	<br />

	<IG name="otp_1" label="Current Email OTP" {error} let:id>
		<input type="text" bind:value={form.otp_1} id="otp_1" placeholder="your OTP here" />
	</IG>

	<IG name="otp_2" label="New Email OTP" {error} let:id>
		<input type="text" bind:value={form.otp_2} id="otp_2" placeholder="your OTP here" />
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
	<Email name={user.name} />
</div>

<style>
	.f1 {
		color: var(--ac2);
	}
</style>
