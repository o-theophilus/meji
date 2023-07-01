<script>
	import { tick, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/comp/button.svelte';

	import Info from '$lib/module/info.svelte';
	import Form from '$lib/module/form.svelte';

	export let data;
	let error;

	let name = data.user.name;

	const validate = async () => {
		error = '';
		if (!name) {
			error = 'This field is required';
		}

		!error && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}user_name/${data.user.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ name })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.user);

				$module = {
					module: Info,
					data: {
						status: 'good',
						title: '# Details Changed',
						message: `Your name has been changed successfully`,
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
		<div class="title">Edit Name</div>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="name"> Fullname: </label>
			<input type="text" bind:value={name} id="name" placeholder="Your fullname here" />
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
