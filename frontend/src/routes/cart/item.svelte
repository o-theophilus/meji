<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Quantity from '$lib/item/quantity.svelte';
	import Value from '$lib/item/variation_value.svelte';

	export let item;
	let error = {};
	let timeoutId;

	const change = async (item) => {
		error = {};

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
			error = resp;
		}
	};
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
			<br />
		{/if}

		<div class="line space">
			<div class="line">
				<span class="price">
					₦{item.price.toLocaleString()}
				</span>
				<Quantity
					quantity={item.quantity}
					on:done={(e) => {
						item.quantity = e.detail.quantity;
						clearTimeout(timeoutId);
						timeoutId = setTimeout(() => {
							change(item);
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
		display: flex;
		gap: var(--sp3);
		align-items: center;
	}

	img {
		height: 100px;
		width: 100px;

		border-radius: var(--sp1);
	}
	.details {
		width: 100%;
	}

	.line {
		display: flex;
		align-items: center;
		gap: 0 var(--sp2);
		flex-wrap: wrap;
	}
	.space {
		justify-content: space-between;
	}

	a {
		text-decoration: none;
		color: var(--ac1);
		font-weight: 500;
	}
	.price {
		color: var(--cl3);
	}

	.variation {
		color: var(--ac2);
		display: flex;
		flex-wrap: wrap;
	}
</style>
