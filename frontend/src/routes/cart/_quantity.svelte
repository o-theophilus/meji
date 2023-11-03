<script>
	import { module, user, loading, toast, portal } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import Quantity from '$lib/item/quantity.svelte';

	let item = { ...$module.item };

	let error = {};
	let quantity = item.quantity;

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart_item_quantity`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				key: item.key,
				variation: item.variation,
				quantity
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$user = resp.user;

			item.quantity = quantity;
			$portal = {
				type: 'item',
				data: item
			};

			$module = '';
			$toast = {
				status: 200,
				message: `${item.name} quantity changed`
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Change Quantity</b>
	</svelte:fragment>

	<div class="property">
		<span class="bold"> Price </span>
		₦{item.price.toLocaleString()} per item

		<br />
		<br />

		<span class="bold"> quantity </span>
		<Quantity
			{quantity}
			min={0}
			on:done={(e) => {
				quantity = e.detail.quantity;
			}}
		/>

		<br />

		{#if quantity > 0}
			<span class="bold"> Total </span>
			₦{(item.price * quantity).toLocaleString()}
		{/if}

		{#if error.quantity}
			<p class="error">
				{error.quantity}
			</p>
		{/if}
	</div>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
	{/if}

	<br />

	<Button class="primary" on:click={submit}>
		{#if quantity > 0}
			Submit
		{:else}
			Remove
		{/if}
	</Button>
</Form>

<style>
	.property {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);

		color: var(--ac1);
	}

	.bold {
		font-weight: 500;
		text-transform: capitalize;
	}
</style>
