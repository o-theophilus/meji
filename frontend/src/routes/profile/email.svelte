<script>
	import { module, portal, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/module/info.svelte';

	import Email from './email_email_template.svelte';

	let form = {};
	let error = {};
	let email_template;
	let message;

	const validate_request_otp = () => {
		error = {};
		message = '';

		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'Please enter a valid email';
		} else if (form.email == $module.user.email) {
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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/email`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$portal = resp.user;

			$module = {
				module: Info,
				status: 200,
				title: '# Email Changed',
				message: `your email change was successful`,
				button: [
					{
						name: 'Ok',
						icon: 'ok'
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
		<div class="title">Change Email</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">Change your account Email.</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup">Current Email: {$module.user.email}</div>

		<div class="inputGroup">
			<label for="email"> New Email: </label>
			<input type="email" bind:value={form.email} id="email" placeholder="your new email here" />
			{#if error.email}
				<p class="error">
					{error.email}
				</p>
			{/if}
		</div>
		<Button
			class="primary"
			name="Request OTPs"
			on:click={() => {
				validate_request_otp();
			}}
		/>
		{#if message}
			<div class="inputGroup">
				{message}
			</div>
		{/if}
		<div class="inputGroup">
			<label for="otp_1"> Current Email OTP: </label>
			<input type="text" bind:value={form.otp_1} id="otp_1" placeholder="your OTP here" />
			{#if error.otp_1}
				<p class="error">
					{error.otp_1}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="otp_2"> New Email OTP: </label>
			<input type="text" bind:value={form.otp_2} id="otp_2" placeholder="your OTP here" />
			{#if error.otp_2}
				<p class="error">
					{error.otp_2}
				</p>
			{/if}
		</div>

		<Button
			class="primary"
			name="Submit"
			on:click={() => {
				validate();
			}}
		/>
	</form>
</Form>

<div bind:this={email_template} style="display: none;">
	<Email name={$user.name} />
</div>
