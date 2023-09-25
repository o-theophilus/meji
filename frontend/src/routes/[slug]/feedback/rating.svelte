<script>
	import SVG from '$lib/svg.svelte';
	import Bar from './rating.bar.svelte';

	export let rating;

	let sum = 0;
	let count = 0;

	$: {
		sum = 0;
		count = 0;

		for (const x of Object.entries(rating)) {
			sum += x[0] * x[1];
			count += x[1];
		}

		sum = sum / count;
		sum = sum % 1 == 0 ? sum.toString() : sum.toFixed(1);
	}
</script>

<section>
	<div class="left">
		<span class="gold"> <span class="sum">{sum}</span>/5 </span>
		<SVG type="star" size="30" />
		<span>
			{count} rating{#if count > 1}s{/if}
		</span>
	</div>

	<div class="right">
		{#each Object.entries(rating).reverse() as [name, value]}
			{name}
			<SVG type="star" size="12" />
			<span> ({value})</span>
			{@const width = (value * 100) / count}
			<Bar {width} />
		{/each}
	</div>
</section>

<style>
	section {
		display: flex;
		align-items: center;
		gap: var(--sp3);

		color: var(--ac2);
		fill: var(--cl6);
	}

	.left {
		display: flex;
		align-items: center;
		flex-direction: column;
		gap: var(--sp1);

		padding: var(--sp2);
		flex-shrink: 0;
	}

	.gold {
		color: var(--cl6);
	}
	.sum {
		font-size: 1.2rem;
		font-weight: 600;
	}

	.right {
		display: grid;
		grid-template-columns: min-content min-content min-content auto;
		align-items: center;
		gap: var(--sp1);

		width: 100%;
	}
</style>
