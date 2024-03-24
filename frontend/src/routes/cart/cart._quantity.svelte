<script>
	import { module, user, toast, portal } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import Quantity from '$lib/item/quantity.svelte';

	let item = { ...$module.item };

	let error = {};

	const submit = async (quantity) => {
		let key = `${item.key}_${JSON.stringify(item.variation)}`;
		if (quantity == 0 && $user.cart.includes(key)) {
			$user.cart = $user.cart.filter((i) => i != key);
		}

		item.quantity = quantity;
		$portal = {
			type: 'item',
			data: item
		};

		$module = '';
		$toast = {
			status: 200,
			message: `${item.name} ${quantity > 0 ? 'quantity changed' : 'removed'}`
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

		if (resp.status == 200) {
			$user.cart = resp.user.cart;

			$portal = {
				type: 'items_done',
				data: {
					cart: resp.cart,
					items: resp.items
				}
			};
		} else {
			$toast = {
				status: 400,
				message: resp.error
			};
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Change Quantity</b>
	</svelte:fragment>

	<div class="property">
		<span class="bold"> Price </span>
		₦{item.price.toLocaleString()} per item

		<br />
		<br />

		<span class="bold"> quantity </span>
		<Quantity
			quantity={item.quantity}
			min={0}
			on:done={(e) => {
				item.quantity = e.detail.quantity;
			}}
		/>

		<br />

		{#if item.quantity > 1}
			<span class="bold"> Total </span>
			₦{(item.price * item.quantity).toLocaleString()}
		{/if}

		{#if error.quantity}
			<p class="error">
				{error.quantity}
			</p>
		{/if}
	</div>

	<!-- {#if error.error}
		<p class="error">
			{error.error}
		</p>
	{/if} -->

	<br />

	<div class="line">
		{#if item.quantity > 0}
			<Button
				class="primary"
				on:click={() => {
					submit(item.quantity);
				}}>Ok</Button
			>
		{/if}

		<Button
			class="hover_red"
			on:click={() => {
				submit(0);
			}}>Remove</Button
		>
	</div>
</Form>

<style>
	.property {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);

		color: var(--ac1);
	}

	.bold {
		font-weight: 500;
		text-transform: capitalize;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
