<script>
	import { flip } from 'svelte/animate';
	import { backInOut } from 'svelte/easing';

	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';
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

<svelte:head>
	<title>Cart | Meji</title>
</svelte:head>

{error}
<Card>
	<Title title="Cart" />
	<Body>
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
	</Body>
	{#if $user.cart.length > 0}
		<Checkout {total} />
	{/if}
</Card>
