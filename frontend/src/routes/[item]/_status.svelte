<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/module/info.svelte';

	let { item } = $module;
	let error = {};
	let all_status = ['live', 'draft', 'delete'];

	const validate = (status) => {
		error = {};
		if (status == 'live') {
			if (item.photos.length == 0) {
				error.error = 'a photo is required';
			}
			if (!item.price) {
				error.error = 'a price is required';
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

			$module = {
				module: Info,
				status: 200,
				title: '# Details Changed',
				message: 'item status has been changed successfully',
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
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
		{#each all_status as s}
			{#if s != item.status}
				<Button
					name={s.charAt(0).toUpperCase() + s.slice(1)}
					on:click={() => {
						validate(s);
					}}
				/>
			{/if}
		{/each}
	</div>

	{#if error.error}
		<br />
		<p class="error">
			{error.error}
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
