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
	import Info from '$lib/info.svelte';

	let emit = createEventDispatcher();

	export let items;
	export let live_items;
	export let total;
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
			₦{total.toLocaleString()}
		</div>
	</div>

	<br />

	<Button
		primary
		on:click={() => {
			if (live_items.length == 0) {
				$module = {
					module: Info,
					status: 400,
					title: 'Empty Cart',
					message: `The item${items.length > 1 ? 's' : ''} in the cart ${
						items.length > 1 ? 'are' : 'is'
					} unavailable`,
					button: [
						{
							name: 'Ok',
							icon: 'ok',
							fn: () => {
								$module = '';
							}
						}
					]
				};
			} else if (!$user.login) {
				$module = {
					module: Login,
					message: 'please login to checkout'
				};
			} else {
				emit('next');
			}
		}}
	>
		<SVG icon="cart_out" />
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
