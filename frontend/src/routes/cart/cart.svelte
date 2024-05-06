<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { user, module } from '$lib/store.js';
	import { createEventDispatcher } from 'svelte';

	import Card from '$lib/card.svelte';
	import SVG from '$lib/svg.svelte';
	import Button from '$lib/button/button.svelte';
	import Login from '../auth/login.svelte';
	import Item from './cart.item.svelte';
	import Title from '$lib/title.svelte';

	let emit = createEventDispatcher();

	export let cart;
	export let items;
	let error = {};
</script>

<Card>
	<Title card>
		Item{items.length != 1 || items[0].quantity != 1 ? 's' : ''}
	</Title>

	<div class="items">
		{#each items as item (`${item.key}${JSON.stringify(item.variation)}`)}
			<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				<Item bind:item />
			</div>
		{/each}
	</div>

	<br />

	<div class="total_amount">
		<div class="total">
			Item{#if items.length != 1 || items[0].quantity != 1}s Total{/if} Price
		</div>
		<div class="amount">
			₦{cart.cost_items.toLocaleString()}
		</div>
	</div>

	<br />

	<Button
		primary
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

		padding-top: var(--sp2);
		border-top: 2px solid var(--ac4);
	}

	.amount {
		font-weight: 700;
		font-size: large;
	}
</style>
