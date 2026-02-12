<script>
	import { Icon } from '$lib/macro';

	let { value = $bindable() } = $props();
</script>

<div class="stars">
	{#each Array(5) as _, i}
		<button class="star" class:active={i < value} onclick={() => (value = i + 1)}>
			<Icon icon="Star" size="28"></Icon>
		</button>
	{/each}
</div>

<style>
	.stars {
		display: flex;
	}

	.star {
		all: unset;
		--icon-stroke-width: 1;
		--icon-fill: var(--ft2);
		--icon-stroke: var(--ft2);

		cursor: pointer;
		line-height: 0;
	}
	.active {
		--icon-fill: goldenrod;
		--icon-stroke: goldenrod;
	}
	.star:hover {
		--icon-fill: gold;
		--icon-stroke: gold;
	}
</style>
