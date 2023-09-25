<script>
	import SVG from '$lib/svg.svelte';

	export let rating = 0;
	export let count = 0;
	export let slug = '';

	let _type = 1;
	export { _type as type };
</script>

{#if rating > 0}
	{#if slug}
		<a class:two={_type != 1} href="/{slug}/feedback">
			{rating.toFixed(1)}
			<SVG type="star" />

			{#if count}
				{count}
				rating{#if count > 1}s{/if}
			{/if}
		</a>
	{:else}
		<div class:two={_type != 1} href="/{slug}/feedback">
			{rating.toFixed(1)}
			<SVG type="star" />

			{#if count}
				{count}
				rating{#if count > 1}s{/if}
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

		font-size: small;
		padding: var(--sp1);
		text-decoration: none;
		color: var(--ac3);

		fill: var(--cl6);
	}

	.two {
		width: 100%;
	}
	.two:hover {
		background-color: var(--ac4);
	}
</style>
