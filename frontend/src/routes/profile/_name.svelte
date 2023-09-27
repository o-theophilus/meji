<script>
	import { portal, module, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';

	let error = {};
	let { name } = $module.user;

	const validate = async () => {
		error = {};
		if (!name) {
			error.name = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${$module.user.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ name })
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
				message: `Name changed`
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Name</b>
	</svelte:fragment>

	<IG name="name" {error} let:id>
		<input bind:value={name} {id} type="text" placeholder="Your fullname here" />
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" on:click={validate}>Save</Button>
</Form>

<style>
</style>
