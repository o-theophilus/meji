<script>
	import { module, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button/button.svelte';
	import ShowPassword from '$lib/button/show_password.svelte';
	import IG from '$lib/input_group.svelte';

	let form = {
		permissions: $module.permissions
	};
	let error = {};
	let show_password = false;

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/permission/${$module.key}`, {
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
			$module = '';
			$toast = {
				status: 200,
				message: 'Permissions saved'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Accept Permissions</b>
	</svelte:fragment>

	<IG
		name="password"
		{error}
		bind:value={form.password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	>
		<svelte:fragment slot="pos_1">
			<ShowPassword bind:show_password />
		</svelte:fragment>
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button primary on:click={validate}>Ok</Button>
</Form>

<style>
</style>
