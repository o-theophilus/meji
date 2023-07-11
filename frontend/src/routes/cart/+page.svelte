<script>
	import { flip } from 'svelte/animate';
	import { backInOut } from 'svelte/easing';

	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Checkout from './checkout.svelte';
	import Item from './item.svelte';

	let total = 0;
	let error = '';

	$: {
		total = 0;
		for (const i in $user.cart) {
			total += $user.cart[i].quantity * $user.cart[i].price;
		}
	}
	const change = async (item, quantity) => {
		item.quantity = quantity;

		if (item.quantity > 0) {
			for (const i in $user.cart) {
				if ($user.cart[i].key == item.key && $user.cart[i].variation == item.variation) {
					$user.cart[i] = item;
					break;
				}
			}
		} else {
			$user.cart = $user.cart.filter((i) => i.key != item.key || i.variation != item.variation);
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(item)
		});

		resp = await resp.json();
		if (resp.status == 200) {
			$user = resp.user;
		} else {
			error = resp.error;
		}
	};
</script>

<Meta title="Cart" description="Cart" />

{error}
<Card>
	<div class="title">Cart</div>
	<div class="items">
		{#each $user.cart as item (`${item.key}${JSON.stringify(item.variation)}`)}
			<div animate:flip={{ delay: 0, duration: 250, easing: backInOut }}>
				<Item
					{item}
					on:done={(e) => {
						change(item, e.detail.quantity);
					}}
				/>
			</div>
		{:else}
			no item here
		{/each}
	</div>
	{#if $user.cart.length > 0}
		<Checkout {total} />
	{/if}
</Card>

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
	}

	.items {
		display: grid;
		gap: var(--sp2);

		margin-top: var(--sp4);
	}
</style>
