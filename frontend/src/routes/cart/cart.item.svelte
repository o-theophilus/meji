<script>
	import { module } from '$lib/store.js';

	import Quantity from './cart._quantity.svelte';
	import Value from '$lib/item/variation_value.svelte';
	import Button from '$lib/button/button.svelte';

	export let item;
</script>

<section>
	<a href="/{item.slug}">
		<img
			src={`${item.photo}/200` || '/image/item.png'}
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

				x &nbsp;

				<Button
					size="small"
					on:click={() => {
						$module = {
							module: Quantity,
							item
						};
					}}
				>
					{item.quantity}
				</Button>
			</div>
			₦{(item.price * item.quantity).toLocaleString()}
		</div>
	</div>
</section>

<style>
	section {
		--height: 80px;
		display: flex;
		gap: var(--sp3);
		align-items: center;

		padding-bottom: var(--sp2);
		border-bottom: 2px solid var(--ac5);
	}

	img {
		width: var(--height);
		height: var(--height);

		border-radius: var(--sp0);
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
		flex-wrap: wrap;
	}
	.price {
		margin-top: auto;
		justify-content: space-between;
	}

	a {
		text-decoration: none;
		color: var(--ac1);
		font-weight: 700;
	}

	.variation {
		display: flex;
		flex-wrap: wrap;
	}
</style>
