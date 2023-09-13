<script>
	import { loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';
	import ShowPassword from '$lib/button.show_password.svelte';

	let password;
	let error = {};
	let show_password = false;

	const validate = () => {
		error = {};

		if (!password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ password })
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

	<IG name="password" {error} let:id>
		<div class="password">
			{#if show_password}
				<input bind:value={password} {id} type="text" placeholder="Password here" />
			{:else}
				<input bind:value={password} {id} type="password" placeholder="Password here" />
			{/if}
			<ShowPassword bind:show_password />
		</div>
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
	.password {
		position: relative;
	}
</style>
