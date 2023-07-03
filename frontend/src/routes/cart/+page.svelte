<script>
	// import { flip } from 'svelte/animate';
	// import { backInOut } from 'svelte/easing';

	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';
	import Checkout from './checkout.svelte';
	import Item from './item.svelte';

	$: $user = $user ? $user : $user;
	let total = 0;
	let error = '';

	$: {
		total = 0;
		for (const i in $user.cart) {
			total += $user.cart[i].quantity * $user.cart[i].price;
		}
	}
	const change = async (item, quantity) => {
		for (const i in $user.cart) {
			if ($user.cart[i].key == item.key && $user.cart[i].variation == item.variation) {
				$user.cart[i].quantity = quantity;
				break;
			}
		}

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}cart/${item.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(item)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$user = resp.data.user;
			} else {
				error = resp.message;
			}
		}
	};

	const remove = async (_item) => {
		$user.cart = $user.cart.filter(
			(item) => item.key != _item.key || item.variation != _item.variation
		);

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}cart/${_item.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(_item)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$user = resp.data.user;
			} else {
				error = resp.message;
			}
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
		{#each $user.cart as item, i (i)}
			<!-- <div animate:flip={{ delay: 0, duration: 250, easing: backInOut }}>
			</div> -->
			<Item
				{item}
				on:mod={(e) => {
					change(item, e.detail);
				}}
				on:del={() => {
					remove(item);
				}}
			/>
		{:else}
			no item here
		{/each}
	</Body>
	{#if $user.cart.length > 0}
		<Checkout {total} />
	{/if}
</Card>
