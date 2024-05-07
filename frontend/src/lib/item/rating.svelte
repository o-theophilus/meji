<script>
	import SVG from '$lib/svg.svelte';

	export let ratings = [];
	export let rating = 0;
	export let href = '';

	let sum = 0;

	for (const x of ratings) {
		sum += x;
	}

	if (sum > 0) {
		sum /= ratings.length;
		sum = sum % 1 == 0 ? sum.toString() : sum.toFixed(1);
	} else {
		sum = rating;
	}
</script>

{#if sum > 0}
	{#if href}
		<a {href}>
			{sum}
			<SVG icon="star" />
		</a>
	{:else}
		<div>
			{sum}
			<SVG icon="star" />
			{#if ratings.length > 0}
				( {ratings.length} rating{#if ratings.length > 1}s{/if} )
			{/if}
		</div>
	{/if}
{/if}

<style>
	a,
	div {
		display: flex;
		align-items: center;
		gap: 4px;

		font-size: small;
		color: var(--ac3);
		fill: var(--cl6);
	}

	a {
		justify-content: center;
		padding: var(--sp1);

		text-decoration: none;
		width: 100%;
	}
	a:hover {
		background-color: var(--ac4);
	}
</style>
