<script>
	import { portal } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Center from '$lib/center.svelte';

	import Cart from './cart.svelte';
	import Delivery from './delivery.svelte';
	import Pay from './pay.svelte';

	export let data;
	let { cart } = data;
	let { previous_receivers } = data;

	$: if ($portal) {
		if ($portal.type == 'item') {
			let items = [];
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
			}
			cart.items = items;
		}

		if ($portal.type == 'receiver') {
			cart.receiver = $portal.data;
		}

		$portal = '';
	}
</script>

<Meta title="Cart" description="Cart" />

<Center>
	<br />
	<div class="ctitle">Cart</div>
</Center>

<Cart {cart} />
<Delivery {cart} {previous_receivers} />
<Pay {cart} />

<style>
</style>
