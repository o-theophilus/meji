<script>
	import { module } from '$lib/store.svelte.js';
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	import Value from '../[slug]/variation/value.svelte';
	import Quantity from './quantity.svelte';

	let { item } = $props();
	let total = item.price * item.quantity;

	let src = $state(item.photo ? `${item.photo}/500` : '/no_photo.png');
</script>

<div class="item">
	<a class="img" href="/{item.slug}">
		<img {src} loading="lazy" alt={item.name} />
	</a>

	<div class="details">
		<div class="name_quantity">
			<div>
				<a class="name" href="/{item.slug}">
					{item.name}
				</a>
				<div class="variation">
					{#each Object.entries(item.variation) as [key, value], i}
						{#if i != 0},{/if}
						{key}: <Value {value} small></Value>
					{/each}
				</div>
			</div>
			<Button onclick={() => module.open(Quantity, item)}>
				Quantity: {item.quantity}
			</Button>
		</div>

		<div class="line space">
			<div class="price">
				{#if item.price}
					₦{item.price.toLocaleString()}
				{/if}
			</div>

			<div class="total">
				₦{total.toLocaleString()}
			</div>
		</div>
	</div>
</div>

<style>
	.item {
		display: flex;
		gap: 16px;

		padding: 16px;
		margin: 8px 0;
		border-radius: 8px;
		background-color: var(--bg1);
	}

	.img {
		display: flex;
		width: 120px;
		height: 120px;
		flex-shrink: 0;
	}

	img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		background-color: var(--bg1);
		border-radius: 4px;
		line-height: 100%;

		outline: 2px solid transparent;
		outline-offset: 2px;
		transition: outline-color var(--trans);
	}

	a:hover img {
		outline-color: var(--ft1);
	}

	.details {
		display: flex;
		flex-direction: column;
		justify-content: space-between;

		width: 100%;
	}
	.name_quantity {
		display: flex;
		gap: 8px;
		justify-content: space-between;
	}

	.name {
		display: block;
		text-decoration: none;
		color: var(--ft2);
	}

	.variation {
		font-size: 0.8rem;
	}

	.price {
		font-weight: 700;
		color: var(--ft1);
	}
</style>
