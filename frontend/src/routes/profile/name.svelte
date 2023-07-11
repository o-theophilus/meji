<script>
	import { portal, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';

	import Info from '$lib/module/info.svelte';
	import Form from '$lib/module/form.svelte';

	let error = {};
	let name = $module.user.name;

	const validate = async () => {
		error = {};
		if (!name) {
			error.name = 'This field is required';
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
			body: JSON.stringify({ name })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$portal = resp.user;

			$module = {
				module: Info,
				status: 200,
				title: '# Details Changed',
				message: `Your name has been changed successfully`,
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
		<div class="title">Edit Name</div>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="name"> Fullname: </label>
			<input type="text" bind:value={name} id="name" placeholder="Your fullname here" />
			{#if error.name}
				<p class="error">
					{error.name}
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
