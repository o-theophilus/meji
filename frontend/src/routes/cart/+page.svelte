<script>
	import { user, portal } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Center from '$lib/center.svelte';
	import Card from '$lib/card.svelte';

	import Cart from './cart.svelte';
	import Delivery from './delivery.svelte';
	import Pay from './pay.svelte';

	export let data;
	let { cart } = data;
	let { items } = data;

	let prev = {
		loaded: false,
		receivers: []
	};

	$: if ($portal) {
		if ($portal.type == 'item') {
			let temp_items = [];
			let temp_cart = [];
			let temp_cost = 0;

			for (const x in items) {
				let xid = `${items[x].key}_${JSON.stringify(items[x].variation)}`;
				if (xid == `${$portal.data.key}_${JSON.stringify($portal.data.variation)}`) {
					items[x].quantity = $portal.data.quantity;
					if (items[x].quantity > 0) {
						temp_items.push(items[x]);
						temp_cart.push(xid);
					}
				} else {
					temp_items.push(items[x]);
					temp_cart.push(xid);
				}

				temp_cost += items[x].quantity * items[x].price;
			}

			items = temp_items;
			$user.cart = temp_cart;
			cart.cost_items = temp_cost;

			if (items.length == 0) {
				cart = null;
			}
		} else if ($portal.type == 'items_quantity') {
			cart = $portal.data.cart;
			items = $portal.data.items;
		} else if ($portal.type == 'prev') {
			prev = $portal.data;
		} else if ($portal.type == 'receiver') {
			cart.name = $portal.data.name;
			cart.phone = $portal.data.phone;
			cart.line = $portal.data.line;
			cart.country = $portal.data.country;
			cart.state = $portal.data.state;
			cart.local_area = $portal.data.local_area;
			cart.postal_code = $portal.data.postal_code;
		} else if ($portal.type == 'pay_account') {
			cart.pay_account = $portal.data.pay_account;
		}

		$portal = '';
	}

	let state = 0;
</script>

<Meta title="Cart" description="Cart" />
{#if cart}
	<Log action="viewed" entity_key={cart.key} entity_type="cart" />
{/if}

<Center>
	<br />
	<div class="ctitle">Cart</div>
</Center>

{#if !cart}
	<Card>no item here</Card>
{:else if state == 0}
	<Cart
		{cart}
		{items}
		on:next={() => {
			state = 1;
		}}
	/>
{:else if state == 1}
	<Delivery
		{cart}
		{prev}
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
		{items}
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
