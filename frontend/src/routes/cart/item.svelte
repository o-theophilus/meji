<script>
	import Quantity from '$lib/quantity.svelte';
	import Value from '$lib/item/variation_value.svelte';

	export let item;
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
				<Quantity quantity={item.quantity} on:done />
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
