<script>
	import { portal, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';

	import Info from '$lib/module/info.svelte';
	import Form from '$lib/module/form.svelte';

	let error = {};
	let phone = $module.user.phone;

	const validate = async () => {
		error = {};
		if (!phone) {
			error.phone = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${$module.user.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ phone })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$portal = resp.user;

			$module = {
				module: Info,
				status: 200,
				title: '# Details Changed',
				message: `Your phone number has been changed successfully`,
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
		<div class="title">Edit Phone Number</div>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="phone"> Phone: </label>
			<input type="tel" bind:value={phone} id="phone" placeholder="Your phone here" />
			{#if error.phone}
				<p class="error">
					{error.phone}
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
