<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';

	let item = { ...$module.item };
	let error = {};

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ info: item.info })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = resp.item;

			$module = '';
			$toast = {
				status: 200,
				message: 'Information changed'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Item</b>
	</svelte:fragment>

	<IG name="info" {error} let:id>
		<textarea bind:value={item.info} {id} placeholder="Information here" />
	</IG>
	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}
	<Button class="primary" name="Submit" on:click={submit} />
</Form>
