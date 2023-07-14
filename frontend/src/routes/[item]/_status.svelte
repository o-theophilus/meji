<script>
	import { module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';

	let { item } = $module;
	let error = {};
	let status_ = ['live', 'draft', 'delete'];

	const submit = async (status) => {
		error = {};
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item_/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ status })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			tick(resp.item);
			$module = '';
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Change Status</div>
	</svelte:fragment>

	<svelte:fragment slot="info">
		Status - {item.status}
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup horizontal">
			{#each status_ as s}
				{#if s != item.status && item.photos.length > 0}
					<Button
						name={s.charAt(0).toUpperCase() + s.slice(1)}
						on:click={() => {
							submit(s);
						}}
					/>
				{/if}
			{/each}

			{#if error.error}
				<p class="error">
					{error.error}
				</p>
			{/if}
		</div>
	</form>
</Form>

<style>
</style>
