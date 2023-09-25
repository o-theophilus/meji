<script>
	import SVG from '$lib/svg.svelte';
	import Bar from './rating.bar.svelte';

	export let feedbacks = [];

	let ratings = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
	let sum = 0;

	$: {
		ratings = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
		sum = 0;
		for (let i of feedbacks) {
			sum += i.rating;
			ratings[i.rating]++;
		}
		sum = sum > 0 ? (sum / feedbacks.length).toFixed(1) : 0;
	}
</script>

<section>
	<div class="left">
		<span class="gold"> <span class="sum">{sum}</span>/5 </span>
		<SVG type="star" size="30" />
		<span>
			{feedbacks.length} rating{#if feedbacks.length > 1}s{/if}
		</span>
	</div>

	<div class="right">
		{#each Object.entries(ratings).reverse() as [name, value]}
			{name}
			<SVG type="star" size="12" />
			<span> ({value})</span>
			{@const width = (value * 100) / feedbacks.length}
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
