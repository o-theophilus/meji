<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { user, module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import SVG from '$lib/svg.svelte';
	import Center from '$lib/center.svelte';
	import Item from './item.svelte';
	import Button from '$lib/button.svelte';
	import Login from '../auth/login.svelte';

	export let data;
	$: items = data.items;
	let error = {};
	let total = 0;

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
				goto(`/orders/${resp.order_key}`);
			} else {
				error = resp;
			}
		}
	};
</script>

<Meta title="Cart" description="Cart" />

<Center>
	<br />
	<div class="ctitle">Cart</div>
</Center>

<Card>
	<div class="items">
		{#each items as item, i (`${item.key}${JSON.stringify(item.variation)}`)}
			<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				<Item
					bind:item
					on:remove={() => {
						items = items.filter((i) => i.key != item.key && i.variation != item.variation);
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

		<Button class="primary" on:click={submit}>
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
