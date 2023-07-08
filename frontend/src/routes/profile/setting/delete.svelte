<script>
	import { token } from '$lib/cookie.js';
	import { user } from '$lib/store.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';

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
			$user = resp.data.user;
			document.location = '/';
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">Delete Account</svelte:fragment>
	<svelte:fragment slot="desc">Are you sure you want to delete account?</svelte:fragment>
	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="password"> Password: </label>
			<input type="password" bind:value={password} id="password" placeholder="Your password here" />
			{#if error.password}
				<p class="error">
					{error.password}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button
				name="Delete"
				on:click={() => {
					validate();
				}}
			/>
		</div>
	</form>
</Form>
