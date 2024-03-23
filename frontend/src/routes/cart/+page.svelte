<script>
	import { portal } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Center from '$lib/center.svelte';
	import Card from '$lib/card.svelte';

	import Cart from './cart.svelte';
	import Delivery from './delivery.svelte';
	import Pay from './pay.svelte';

	export let data;
	let { cart } = data;
	let { previous_receivers } = data;

	$: if ($portal) {
		if ($portal.type == 'item') {
			let items = [];
			cart.transaction.total_items = 0;
			for (const x in cart.items) {
				if (
					`${cart.items[x].key}_${JSON.stringify(cart.items[x].variation)}` ==
					`${$portal.data.key}_${JSON.stringify($portal.data.variation)}`
				) {
					cart.items[x].quantity = $portal.data.quantity;
					if (cart.items[x].quantity > 0) {
						items.push(cart.items[x]);
					}
				} else {
					items.push(cart.items[x]);
				}

				cart.transaction.total_items += cart.items[x].quantity * cart.items[x].price;
			}
			cart.items = items;
		} else {
			cart = $portal.data;
		}

		$portal = '';
	}

	let state = 0;
</script>

<Meta title="Cart" description="Cart" />

<Center>
	<br />
	<div class="ctitle">Cart</div>
</Center>

{#if !cart}
	<Card>no item here</Card>
{:else if state == 0}
	<Cart
		{cart}
		on:next={() => {
			state = 1;
		}}
	/>
{:else if state == 1}
	<Delivery
		{cart}
		{previous_receivers}
		on:next={() => {
			state = 2;
		}}
		on:back={() => {
			state = 0;
		}}
	/>
{:else if state == 2}
	<Pay
		{cart}
		on:back={() => {
			state = 1;
		}}
	/>
{/if}

<style>
	.ctitle {
		text-transform: capitalize;
	}
</style>
