<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';

	let item = { ...$module.item };
	let error = {};

	const validate = async () => {
		error = {};

		if (item.price && (!Number.isFinite(item.price) || item.price < 0)) {
			error.price = 'please enter a valid price';
		}

		if (item.old_price) {
			if (!Number.isFinite(item.old_price) || item.old_price < 0) {
				error.old_price = 'please enter a valid price';
			} else if (item.old_price <= item.price) {
				error.old_price = 'old price should be greater than price';
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				price: item.price,
				old_price: item.old_price
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'item',
				data: resp.item
			};
			$module = '';
			$toast = {
				status: 200,
				message: 'Price changed'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Price</b>
	</svelte:fragment>

	<IG name="price" {error} bind:value={item.price} type="number" placeholder="Price here" />

	<IG
		name="old price"
		{error}
		bind:value={item.old_price}
		type="number"
		placeholder="Old price here"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" on:click={validate}>Save</Button>
</Form>
