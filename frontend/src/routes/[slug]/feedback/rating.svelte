<script>
	import SVG from '$lib/comp/svg.svelte';
	import Bar from './rating.bar.svelte';

	export let feedbacks = [];

	let five = 0;
	let four = 0;
	let three = 0;
	let two = 0;
	let one = 0;

	for (let i in feedbacks) {
		if (feedbacks[i].rating == 5) {
			five++;
		} else if (feedbacks[i].rating == 4) {
			four++;
		} else if (feedbacks[i].rating == 3) {
			three++;
		} else if (feedbacks[i].rating == 2) {
			two++;
		} else {
			one++;
		}
	}

	let sum = five * 5 + four * 4 + three * 3 + two * 2 + one * 1;
	let mean = 0;
	if (sum > 0 && feedbacks.length > 0) {
		mean = (sum / feedbacks.length).toFixed(1);
	}
</script>

<section>
	<div class="left">
		<div class="rating">
			<strong>{mean}</strong>/5
		</div>
		<div class="svg">
			<SVG type="star" size="30" />
		</div>
		<div class="small_rating">
			{feedbacks.length} rating{#if feedbacks.length > 1}s{/if}
		</div>
	</div>
	<div class="right">
		<Bar id={5} value={five} width={(five * 100) / feedbacks.length} />
		<Bar id={4} value={four} width={(four * 100) / feedbacks.length} />
		<Bar id={3} value={three} width={(three * 100) / feedbacks.length} />
		<Bar id={2} value={two} width={(two * 100) / feedbacks.length} />
		<Bar id={1} value={one} width={(one * 100) / feedbacks.length} />
	</div>
</section>

<style>
	section {
		display: flex;
		align-items: center;

		gap: var(--sp3);
	}

	.left {
		display: flex;
		align-items: center;
		flex-direction: column;
		gap: var(--sp1);

		padding: var(--sp2);

		border-radius: var(--sp0);
		border: 2px solid var(--ac5);
		/* box-shadow: var(--shad1); */
	}
	.right {
		display: flex;
		flex-direction: column;
		gap: 4px;

		width: 100%;
	}
	.rating {
		color: var(--cl6);
	}
	strong {
		font-size: 1.2rem;
	}
	.svg {
		fill: var(--cl6);
	}
	.small_rating {
		width: max-content;
	}
</style>
