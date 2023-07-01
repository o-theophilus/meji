<script>
	import { user, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/comp/button.svelte';

	import Info from '$lib/module/info.svelte';
	import Form from '$lib/module/form.svelte';

	let error;
	let phone = $user.phone;

	const validate = async () => {
		error = '';
		if (!phone) {
			error = 'This field is required';
		}

		!error && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}user_phone`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ phone })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$user = resp.data.user;

				$module = {
					module: Info,
					data: {
						status: 'good',
						title: '# Details Changed',
						message: `Your phone number has been changed successfully`,
						button: [
							{
								name: 'Ok',
								icon: 'ok'
							}
						]
					}
				};
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Edit Phone Number</div>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="phone"> Phone: </label>
			<input type="tel" bind:value={phone} id="phone" placeholder="Your phone here" />
			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button name="Save" class="primary" />
		</div>
	</form>
</Form>

<style>
</style>
