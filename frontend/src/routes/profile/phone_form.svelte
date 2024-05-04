<script>
	import { portal, module, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Form from '$lib/form.svelte';

	let error = {};
	let form = { phone: $module.user.phone };

	const validate = async () => {
		error = {};
		if (!form.phone) {
			error.phone = 'this field is required';
		} else if (form.phone == $module.user.phone) {
			error.phone = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${$module.user.key}`, {
			method: 'put',
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
				message: 'Phone number changed'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Phone Number</b>
	</svelte:fragment>

	<IG name="phone" {error} bind:value={form.phone} type="tel" placeholder="Your phone here" />

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button primary on:click={validate}>Save</Button>
</Form>

<style>
</style>
