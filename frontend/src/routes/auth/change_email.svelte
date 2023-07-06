<script>
	import { module, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';

	import Info from '$lib/module/info.svelte';

	let email;
	let error = '';

	export let data;

	const validate = async () => {
		error = '';

		if (!email) {
			error = 'This field is required';
		} else if (!/\S+@\S+\.\S+/.test(email)) {
			error = 'Please enter a valid email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}email/${data.token}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ email })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$user = resp.data.user;

				$module = {
					module: Info,
					data: {
						status: 'good',
						title: '# Email Changed',
						message: `your email change was successful`,
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
				$module = {
					module: Info,
					data: {
						status: 'bad',
						title: `Invalid or Expired Token`,
						message: `
**Invalid or Expired Token**;
There was an error while reading the token.

Please try again repeacting the action.`,
						button: [
							{
								name: 'Ok',
								icon: 'ok'
							}
						]
					}
				};
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Change Email</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">Change your account Email.</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="email"> Email: </label>
			<input type="email" bind:value={email} id="email" placeholder="Your email here" />
			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" />
		</div>
	</form>
</Form>
