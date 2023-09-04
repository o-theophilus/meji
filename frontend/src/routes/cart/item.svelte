<script>
	import { user, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	import Quantity from '$lib/item/quantity.svelte';
	import Value from '$lib/item/variation_value.svelte';

	const emit = createEventDispatcher();

	export let item;

	const equal = (obj1, obj2) => {
		const keys1 = Object.keys(obj1);
		const keys2 = Object.keys(obj2);

		if (keys1.length !== keys2.length) {
			return false;
		}

		for (const key of keys1) {
			if (obj1[key] !== obj2[key]) {
				return false;
			}
		}

		return true;
	};

	const change = async (qty) => {
		counter += 1;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				key: item.key,
				variation: item.variation,
				quantity: qty
			})
		});
		resp = await resp.json();
		counter -= 1;

		if (resp.status == 200) {
			$user = resp.user;
			for (const x in $user.cart) {
				for (const y in resp.user.cart) {
					if (
						counter == 0 &&
						$user.cart[x].key == item.key &&
						resp.user.cart[y].key == item.key &&
						equal($user.cart[x].variation, item.variation) &&
						equal(resp.user.cart[y].variation, item.variation)
					) {
						$user.cart[x].quantity = resp.user.cart[y].quantity;
						item.quantity = resp.user.cart[y].quantity;
					}
				}
			}
		} else {
			for (const x in $user.cart) {
				if ($user.cart[x].key == item.key && equal($user.cart[x].variation, item.variation)) {
					item.quantity = $user.cart[x].quantity;
				}
			}

			$toast = {
				status: 400,
				message: 'Error updating cart'
			};
		}
	};

	let timer;
	let counter = 0;
</script>

<section>
	<a href="/{item.slug}">
		<img
			src={`${item.photos[0]}/200` || '/image/item.png'}
			alt={item.name}
			onerror="this.src='/image/item.png'"
		/>
	</a>
	<div class="details">
		<div>
			<a href="/{item.slug}">
				{item.name}
			</a>

			{#if Object.keys(item.variation).length > 0}
				<div class="variation">
					{#each Object.entries(item.variation) as [key, value], i}
						{#if i != 0},{/if}
						{key}: &nbsp;<Value {value} />
					{/each}
				</div>
			{/if}
		</div>

		<div class="line price">
			<div class="line">
				₦{item.price.toLocaleString()}
				<Quantity
					quantity={item.quantity}
					on:done={(e) => {
						if (e.detail.quantity > 0) {
							item.quantity = e.detail.quantity;
						} else {
							emit('remove');
						}

						clearTimeout(timer);
						timer = setTimeout(() => {
							change(e.detail.quantity);
						}, 1000);
					}}
				/>
			</div>
			₦{(item.price * item.quantity).toLocaleString()}
		</div>
	</div>
</section>

<style>
	section {
		--height: 100px;
		display: flex;
		gap: var(--sp3);
		align-items: center;
	}

	img {
		width: 100px;
		height: var(--height);

		border-radius: var(--sp1);
	}
	.details {
		display: flex;
		flex-direction: column;
		justify-content: space-between;

		width: 100%;
		min-height: var(--height);
	}

	.line {
		display: flex;
		align-items: center;
		gap: 0 var(--sp2);
		flex-wrap: wrap;
	}
	.price {
		margin-top: auto;
		justify-content: space-between;
	}

	a {
		text-decoration: none;
		color: var(--ac1);
		font-weight: 500;
	}

	.variation {
		color: var(--ac2);
		display: flex;
		flex-wrap: wrap;
	}
</style>
