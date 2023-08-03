<script>
	import { user } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Eta from './eta.svelte';
	import Address from './address.svelte';

	import Item from './items.svelte';
	import Total from './total.svelte';
	import Action from './action.svelte';

	export let data;
	let { order } = data;
	let { previous_recipients } = data;
</script>

<Meta title="Order" description="Order" />

<Card>
	<b>
		Order ID: {order.key}
	</b>
	<br />
	<br />
	<!-- <section> -->
	<!-- <div class="block"> -->
	<!-- {#if order.status != 'delivered'} -->
	<!-- {/if} -->
	<!-- </div> -->
	<!-- <div class="block"> -->
	<!-- {#if order.status == 'pending'} -->
	<!-- {:else} -->
	<b> Cost Breakdown </b>
	<Item items={order.items} />
	<Total user={$user} {order} />
	<Eta {order} />
	<Address {order} {previous_recipients} />
	<Action {order} />
	<b> Order status </b>
	{order.status}

	<!-- {/if} -->
	<!-- </div> -->
	<!-- </section> -->
</Card>

<style>
	section,
	.block {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		width: 100%;
	}
	section {
		margin-top: var(--sp2);
	}

	@media screen and (min-width: 800px) {
		section {
			flex-direction: unset;
		}
	}
</style>
