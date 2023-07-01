<script>
	import { import.meta.env.VITE_BACKEND } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';

	let password;
	let error;

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}user`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ password })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$token = null;

				document.location = '/';
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">Delete Account</svelte:fragment>
	<svelte:fragment slot="desc">Are you sure you want to delete account?</svelte:fragment>
	<form on:submit|preventDefault={submit} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="password"> Password: </label>
			<input type="password" bind:value={password} id="password" placeholder="Your password here" />
			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button name="Delete" />
		</div>
	</form>
</Form>
