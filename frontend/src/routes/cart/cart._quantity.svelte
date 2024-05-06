<script>
	import { module, user, toast, portal, loading, state } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button/button.svelte';
	import Number from '$lib/number.svelte';
	import IG from '$lib/input_group.svelte';

	let item = { ...$module.item };

	let error = {};

	const submit = async (quantity) => {
		$loading = true;

		let key = `${item.key}_${JSON.stringify(item.variation)}`;
		if (quantity == 0 && $user.cart.includes(key)) {
			$user.cart = $user.cart.filter((i) => i != key);
		}

		item.quantity = quantity;
		$portal = {
			type: 'item',
			data: item
		};

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/quantity`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				key: item.key,
				variation: item.variation,
				quantity
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$user.cart = resp.user.cart;
			$portal = {
				type: 'items_quantity',
				data: {
					cart: resp.cart,
					items: resp.items
				}
			};

			$module = '';
			$toast = {
				status: 200,
				message: `${item.name} ${quantity > 0 ? 'quantity changed' : 'removed'}`
			};

			let i = $state.findIndex((x) => x.name == 'cart');
			if (i != -1) {
				$state[i].loaded = false;
			}
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Change Quantity</b>
	</svelte:fragment>

	{#if item.quantity > 0}
		<span class="bold">Price</span> : ₦{item.price.toLocaleString()}
		{#if item.quantity > 1}
			per item
			<br />
			<span class="bold"> Total </span> : ₦{(item.price * item.quantity).toLocaleString()}
		{/if}

		<br />
		<br />
	{/if}

	<IG name="quantity" {error} let:id>
		<Number bind:value={item.quantity} {id} min={0} />
	</IG>

	{#if error.error}
		<br />
		<p class="error">
			{error.error}
		</p>
	{/if}

	<br />

	<div class="row">
		<Button
			disabled={item.quantity == 0}
			primary
			on:click={() => {
				submit(item.quantity);
			}}>Ok</Button
		>

		<Button
			extra="hover_red"
			on:click={() => {
				submit(0);
			}}>Remove</Button
		>
	</div>
</Form>

<style>
	.bold {
		font-weight: 700;
		text-transform: capitalize;
	}

	.row {
		display: flex;
		gap: var(--sp1);
	}
</style>
