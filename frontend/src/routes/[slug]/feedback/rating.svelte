<script>
	import SVG from '$lib/svg.svelte';
	import Bar from './rating.bar.svelte';

	export let ratings = [];
	let sum = 0;
	let _ratings = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
	let arranged = { ..._ratings };

	$: {
		sum = 0;
		arranged = { ..._ratings };

		for (const x of ratings) {
			sum += x;
			arranged[x]++;
		}

		sum = sum / ratings.length;
		sum = sum % 1 == 0 ? sum.toString() : sum.toFixed(1);
	}
</script>

<section>
	<div class="left">
		<span class="gold"> <span class="sum">{sum}</span>/5 </span>
		<SVG icon="star" size="30" />
		<span>
			{ratings.length} rating{#if ratings.length > 1}s{/if}
		</span>
	</div>

	<div class="right">
		{#each Object.entries(arranged).reverse() as [name, value]}
			{name}
			<SVG icon="star" size="12" />
			<span> ({value})</span>
			{@const width = (value * 100) / ratings.length}
			<Bar {width} />
		{/each}
	</div>
</section>

<style>
	section {
		display: flex;
		align-items: center;
		gap: var(--sp3);

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
		font-weight: 900;
	}

	.right {
		display: grid;
		grid-template-columns: min-content min-content min-content auto;
		align-items: center;
		gap: var(--sp1);

		width: 100%;
	}
</style>
