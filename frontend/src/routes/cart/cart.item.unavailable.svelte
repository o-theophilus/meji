<script>
	import { token } from '$lib/cookie.js';
	import { user, toast, loading, state, portal, module } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';

	export let item;

	const submit = async () => {
		$loading = true;

		$user.cart = $user.cart.filter((i) => i != `${item.key}_${JSON.stringify(item.variation)}`);

		item.quantity = 0;
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
				quantity: item.quantity
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
				message: `${item.name} ${item.quantity > 0 ? 'quantity changed' : 'removed'}`
			};
		} else {
			$toast = {
				status: 400,
				message: resp.error
			};
		}
	};
</script>

<div class="blocker">
	<div class="block">
		Unavailable
		<div class="button">
			<Button size="small" href="/{item.slug}">view</Button>
			<Button size="small" on:click={submit}>Remove</Button>
		</div>
	</div>
</div>

<style>
	.blocker {
		display: flex;
		justify-content: center;
		align-items: center;

		position: absolute;
		inset: 0;
		background-color: color-mix(in srgb, var(--ac4), transparent 40%);
		color: var(--ac1);
	}
	.block {
		display: grid;
		gap: var(--sp1);
		justify-items: center;

		padding: var(--sp2);
		border-radius: var(--sp0);
		background-color: var(--ac6);
	}

	.button {
		display: flex;
		gap: var(--sp1);

		pointer-events: all;
	}
</style>
