<script>
	import { module, portal, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Input from '$lib/input.svelte';
	import EmailTemplate from './email_template.svelte';

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

		$loading = 'requesting OTP . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/email_otp`, {
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
			message =
				'OTP has been sent to your current email and your new email. The OTP will valid for 15 minutes';
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
		} else if (form.email == user.email) {
			error.email = 'please use a different email form your current email';
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
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email`, {
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
			$portal = {
				type: 'user',
				data: resp.user
			};
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

	<span>Current Email: {user.email}</span>

	<br />
	<br />

	<IG name="email" label="New Email" {error} let:id>
		<form on:submit|preventDefault>
			<Input type="email" bind:value={form.email} {id} placeholder="your new email here" />
			<div>
				<Button
					primary={/\S+@\S+\.\S+/.test(form.email) && form.email != user.email}
					on:click={validate_request_otp}
				>
					Request OTPs
				</Button>
			</div>
		</form>
	</IG>

	{#if message}
		<div class="message">
			{message}
		</div>
		<br />
	{/if}

	<IG
		name="otp_1"
		label="Current Email OTP"
		{error}
		type="text"
		bind:value={form.otp_1}
		placeholder="your OTP here"
	/>

	<IG
		name="otp_2"
		label="New Email OTP"
		{error}
		type="text"
		bind:value={form.otp_2}
		placeholder="your OTP here"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button primary on:click={validate}>Save</Button>
</Form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate name={user.name} />
</div>

<style>
	form {
		display: flex;
		gap: var(--sp1);
	}
	form div {
		flex-shrink: 0;
	}

	.message {
		background-color: var(--cl5);
		color: var(--ac6_);
		padding: var(--sp1);
		width: 100%;
	}
</style>
