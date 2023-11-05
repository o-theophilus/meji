<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { page } from '$app/stores';
	import { user, module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import SVG from '$lib/svg.svelte';
	import Button from '$lib/button.svelte';
	import Login from '../auth/login.svelte';
	import Item from './cart.item.svelte';
	import Delivery from './cart.delivery.svelte';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();

	export let cart;

	let error = {};
	let total = 0;

	$: {
		total = 0;
		for (const x in cart.items) {
			total += cart.items[x].quantity * cart.items[x].price;
		}
		total += cart.transaction.delivery_fee;
	}
</script>

<Card>
	<div class="items">
		{#each cart.items as item, i (`${item.key}${JSON.stringify(item.variation)}`)}
			<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				<Item bind:item />
			</div>
		{:else}
			no item here
		{/each}

		{#if cart.items.length > 0}
			<Delivery {cart} />
		{/if}
	</div>

	{#if cart.items.length > 0}
		<div class="total_amount">
			<div class="total">Total Amount</div>
			<div class="amount">
				₦{total.toLocaleString()}
			</div>
		</div>

		<br />

		<Button
			class="primary"
			on:click={() => {
				if ($user.login) {
					emit('next');
				} else {
					$module = {
						module: Login,
						data: {
							message: 'please login to checkout',
							return_url: $page.url.pathname
						}
					};
				}
			}}
		>
			<SVG type="cart_out" />
			Checkout
		</Button>

		{#if error.error}
			<br />
			<span class="error">
				{error.error}
			</span>
		{/if}
	{/if}
</Card>

<style>
	.items {
		display: grid;
		gap: var(--sp2);
	}

	.total_amount {
		display: flex;
		justify-content: space-between;
		align-items: center;

		margin-top: var(--sp3);
		padding-top: var(--sp2);
		border-top: 2px solid var(--ac4);
		color: var(--ac1);
	}

	.amount {
		font-weight: 500;
		font-size: large;
	}
</style>
