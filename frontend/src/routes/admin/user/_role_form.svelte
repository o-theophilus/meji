<script>
	import { tick, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';

	export let data;
	let { user } = data;
	let roles = ['1', '2', '3', 'jump'];

	let selected;
	let error = '';

	const submit = async () => {
		error = '';
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}category/${user.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(user)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.item);
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Edit User Role</div>
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup category">
			{#each roles as role}
				<label class="button" for={role}>
					<input type="checkbox" id={role} value={role} />
					{role}</label
				>
				<!-- bind:group={selected}  -->
			{/each}
		</div>
		{#if error}
			<p class="error">
				{error}
			</p>
		{/if}

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" on:click={submit} />
		</div>
	</form>
</Form>
