<script>
	import { flip } from 'svelte/animate';
	import { backInOut } from 'svelte/easing';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { user, module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Item from './item.svelte';
	import Button from '$lib/button.svelte';
	import Login from '../auth/login.svelte';

	export let data;
	export let { items } = data;
	let total = 0;
	let error = {};

	$: {
		total = 0;
		for (const i in items) {
			total += items[i].quantity * items[i].price;
		}
	}

	const login = async () => {
		$module = {
			module: Login,
			data: {
				message: 'please login to checkout',
				return_url: $page.url.pathname
			}
		};
	};

	const submit = async () => {
		if (!$user.login) {
			login();
		} else {
			$loading = true;
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order`, {
				method: 'post',
				headers: {
					'Content-Type': 'application/json',
					Authorization: $token
				}
			});
			resp = await resp.json();
			$loading = false;

			if (resp.status == 200) {
				$user.cart = [];
				goto(`/profile/orders/${resp.order_key}`);
			} else {
				error = resp;
			}
		}
	};

	const change = async (item, qty) => {
		error = {};
		item.quantity = qty;

		if (qty > 0) {
			for (const x in items) {
				if (items[x].key == item.key && items[x].variation == item.variation) {
					items[x] = item;
					break;
				}
			}
		} else {
			items = items.filter((i) => i.key != item.key && i.variation != item.variation);
			$user.cart = $user.cart.filter((i) => i.key != item.key && i.variation != item.variation);
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
			for (const x in $user.cart) {
				for (const y in items) {
					if ($user.cart[x].key == item.key && items[y].key == item.key) {
						items[y].quantity = $user.cart[x].quantity;
					}
				}
			}
		} else {
			error = resp;
		}
	};
</script>

<Meta title="Cart" description="Cart" />

<Card>
	<div class="title">Cart</div>
	<div class="items">
		{#each items as item (`${item.key}${JSON.stringify(item.variation)}`)}
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

	{#if items.length > 0}
		<div class="total_amount">
			<div class="total">Total Amount</div>
			<div class="amount">
				₦{total.toLocaleString()}
			</div>
		</div>

		<br />

		<Button name="Checkout" icon="cart_out" class="primary" on:click={submit} />

		{#if error.error}
			<br />
			<span class="error">
				{error.error}
			</span>
		{/if}
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

	.total_amount {
		display: flex;
		justify-content: space-between;
		align-items: center;

		margin-top: var(--sp3);
		padding-top: var(--sp2);
		border-top: 2px solid var(--ac4);
	}

	.total,
	.amount {
		font-weight: 500;
	}
	.amount {
		font-size: 1.2rem;
		color: var(--cl3);
	}
</style>
