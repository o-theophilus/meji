<script>
	import { createEventDispatcher } from 'svelte';
	import SVG from '$lib/comp/svg.svelte';

	let emit = createEventDispatcher();

	export let rating = 0;
	const set = (value) => {
		emit('ok', value);
	};
</script>

<section>
	{#each Array(5) as _, i}
		<div
			class="svg"
			class:active={5 - i == rating}
			on:click={() => {
				set(5 - i);
			}}
		>
			<SVG type="star" size="40" />
		</div>
	{/each}
</section>

<style>
	section {
		display: flex;
		flex-direction: row-reverse;

		width: fit-content;
		gap: var(--gap1);
	}
	.svg {
		display: flex;
		align-items: center;

		cursor: pointer;
	}

	.svg.active {
		fill: var(--color6);
	}
	.svg.active ~ .svg {
		fill: var(--color6);
	}

	.svg:hover {
		fill: gold !important;
	}
	.svg:hover ~ .svg {
		fill: gold;
	}
</style>
