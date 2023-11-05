<script>
	import { portal } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Center from '$lib/center.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

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

		if ($portal.type == 'account') {
			cart.transaction.account = $portal.data;
		}

		$portal = '';
	}

	let states = ['cart', 'receiver', 'payment'];
	let state = 0;
</script>

<Meta title="Cart" description="Cart" />

<Center>
	<br />

	<div class="ctitle">
		<div class="ctitle">
			{#if state > 0}
				<Button
					class="round"
					on:click={() => {
						state -= 1;
					}}
				>
					<SVG type="angle" size="10" />
				</Button>
			{/if}

			{states[state]}
		</div>
	</div>
</Center>

{#if state == 0}
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
