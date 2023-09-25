<script>
	import SVG from '$lib/svg.svelte';

	export let rating;
	export let href = '';

	let sum = 0;
	let count = 0;

	$: if (typeof rating == 'object') {
		sum = 0;
		count = 0;

		for (const x of Object.entries(rating)) {
			sum += x[0] * x[1];
			count += x[1];
		}

		sum = sum / count;
		sum = sum % 1 == 0 ? sum.toString() : sum.toFixed(1);
	} else {
		sum = rating;
	}
</script>

{#if sum > 0}
	{#if href}
		<a {href}>
			{sum}
			<SVG type="star" />
		</a>
	{:else}
		<div>
			{sum}
			<SVG type="star" />
			{#if count}
				{count} rating{#if count > 1}s{/if}
			{/if}
		</div>
	{/if}
{/if}

<style>
	a,
	div {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 4px;

		padding: var(--sp1);

		font-size: small;
		color: var(--ac3);
		fill: var(--cl6);
	}

	a {
		text-decoration: none;
		width: 100%;
	}
	a:hover {
		background-color: var(--ac4);
	}
</style>
