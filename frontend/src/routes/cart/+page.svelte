<script>
	import { user, portal } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Center from '$lib/center.svelte';
	import Card from '$lib/card.svelte';
	import Title from '$lib/title.svelte';

	import Cart from './cart.svelte';
	import Delivery from './delivery.svelte';
	import Pay from './pay.svelte';
	import { onMount } from 'svelte';

	export let data;
	let { items } = data;
	let { cart } = data;
	let total = 0;
	let state = 0;
	let prev = {
		loaded: false,
		receivers: []
	};
	let live_items = [];

	onMount(() => {
		for (const x of items) {
			if (x.status == 'live') {
				total += x.quantity * x.price;
				live_items.push(x);
			}
		}

		if (cart) {
			if (cart.delivery_date) {
				cart.delivery_date = new Date(cart.delivery_date);
			} else {
				let temp = new Date();
				temp.setDate(temp.getDate() + 4);
				temp.setHours(10, 0, 0, 0);
				cart.delivery_date = temp;
			}
		}
	});

	$: if ($portal) {
		if ($portal.type == 'item') {
			let temp_items = [];
			let temp_cart = [];
			total = 0;

			for (let x of items) {
				let xid = `${x.key}_${JSON.stringify(x.variation)}`;
				if (xid == `${$portal.data.key}_${JSON.stringify($portal.data.variation)}`) {
					x.quantity = $portal.data.quantity;
					if (x.quantity > 0) {
						temp_items.push(x);
						temp_cart.push(xid);
					}
				} else {
					temp_items.push(x);
					temp_cart.push(xid);
				}
				total += x.quantity * x.price;
			}

			items = temp_items;
			$user.cart = temp_cart;

			if (items.length == 0) {
				cart = null;
			}
		} else if ($portal.type == 'prev') {
			prev = $portal.data;
		} else if ($portal.type == 'items_quantity') {
			cart.pay_account = $portal.data.cart.pay_account;
			items = $portal.data.items;
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
</script>

<Meta title="Cart" description="view / purchase the items in the cart" />
{#if cart}
	<Log action="viewed" entity_key={cart.key} entity_type="cart" />
{/if}

<Center>
	<Title>Cart</Title>
</Center>

{#if !cart}
	<Card>no item here</Card>
{:else if state == 0}
	<Cart
		{total}
		{items}
		{live_items}
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
		items={live_items}
		{total}
		on:back={() => {
			state = 1;
		}}
	/>
{/if}

<style>
</style>
