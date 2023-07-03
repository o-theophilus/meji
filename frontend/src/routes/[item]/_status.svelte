<script>
	import { module, tick } from '$lib/store.js';

	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';

	export let data;
	let { item } = data;

	let error;

	const change_state = async (status) => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}item_/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ status })
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
		<div class="title">Change Status</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">
		Status - {item.status}
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup horizontal">
			{#if 'live' != item.status && item.photos.length > 0}
				<Button
					name={'Go Live'}
					on:click={() => {
						change_state('live');
					}}
				/>
			{/if}
			{#if 'draft' != item.status}
				<Button
					name={'Draft'}
					on:click={() => {
						change_state('draft');
					}}
				/>
			{/if}
			{#if 'delete' != item.status}
				<Button
					name={'Delete'}
					on:click={() => {
						change_state('delete');
					}}
				/>
			{/if}

			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}
		</div>
	</form>
</Form>

<style>
</style>
