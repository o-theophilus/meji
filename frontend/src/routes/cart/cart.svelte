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
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();

	export let cart;

	let error = {};
</script>

<Card>
	<div class="ctitle">Item{cart.items.length ? 's' : ''}</div>

	<br />
	<br />

	<div class="items">
		{#each cart.items as item (`${item.key}${JSON.stringify(item.variation)}`)}
			<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				<Item bind:item />
			</div>
		{/each}
	</div>

	<br />

	<div class="total_amount">
		<div class="total">Item{cart.items.length ? 's' : ''} Total Price</div>
		<div class="amount">
			₦{cart.transaction.total_items.toLocaleString()}
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
					message: 'please login to checkout'
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

		color: var(--ac1);
	}

	.amount {
		font-weight: 500;
		font-size: large;
	}
</style>
