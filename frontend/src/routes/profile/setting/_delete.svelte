<script>
	import { loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';
	import ShowPassword from '$lib/button/show_password.svelte';

	let form = {};
	let error = {};
	let show_password = false;

	const validate = () => {
		error = {};

		if (!form.note) {
			error.note = 'This field is required';
		}

		if (!form.password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'deleting . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$token = resp.data.token;
			document.location = '/';
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b> Delete Account </b>
		Are you sure you want to delete account?
	</svelte:fragment>

	<IG
		name="note"
		label="Please give reason"
		{error}
		type="textarea"
		bind:value={form.note}
		placeholder="Reason"
	/>

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

	<Button on:click={validate}>Delete</Button>
</Form>

<style>
</style>
