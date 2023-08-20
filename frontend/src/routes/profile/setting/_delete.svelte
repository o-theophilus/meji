<script>
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';

	let password;
	let error = {};

	const validate = () => {
		error = {};

		if (!password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ password })
		});
		resp = await resp.json();

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

	<IG name="password" {error} let:id>
		<input bind:value={password} {id} type="password" placeholder="Your password here" />
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button
		name="Delete"
		on:click={() => {
			validate();
		}}
	/>
</Form>
