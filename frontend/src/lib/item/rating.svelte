<script>
	import SVG from '$lib/comp/svg.svelte';

	export let rating = 0;
</script>

<section>
	{rating}
	<div class="svg">
		<SVG type="star" />
	</div>
</section>

<style>
	.svg {
		display: flex;
		align-items: center;

		fill: var(--cl6);
	}
	section {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 4px;
		font-size: small;

		width: fit-content;

		padding: 4px;
		border-radius: var(--brad1);

		background-color: var(--ac5);
	}
</style>
