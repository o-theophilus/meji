<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';

	let item = { ...$module.item };
	let error = {};

	const validate = (status) => {
		error = {};
		if (status == 'live') {
			if (item.photos.length == 0) {
				error.error = 'a photo is required';
			}
			if (!item.price) {
				let err = 'price is required';
				error.error = error.error ? `${error.error}<br/>${err}` : err;
			}
		}

		Object.keys(error).length === 0 && submit(status);
	};

	const submit = async (status) => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ status })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = resp.item;
			$module = '';
			$toast = {
				status: 200,
				message: 'Status changed'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Change Status</b>
		Status - {item.status}
	</svelte:fragment>

	<div class="row">
		{#each ['live', 'draft', 'delete'] as s}
			{#if s != item.status}
				<Button
					on:click={() => {
						validate(s);
					}}
				>
					{s.charAt(0).toUpperCase() + s.slice(1)}
				</Button>
			{/if}
		{/each}
	</div>

	{#if error.error}
		<br />
		<p class="error">
			{@html error.error}
		</p>
	{/if}
</Form>

<style>
	.row {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);
	}
</style>
