<script>
	import SVG from '$lib/svg.svelte';

	export let rating = 0;

	let _type = 1;
	export { _type as type };
</script>

<section class:two={_type != 1}>
	{rating}
	<SVG type="star" />
</section>

<style>
	section {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 4px;

		font-size: small;
		padding: var(--sp1);

		/* padding: 4px; */
		/* border-radius: var(--sp0); */
		/* background-color: var(--ac5); */
		fill: var(--cl6);

		cursor: pointer;
	}

	.two {
		width: 100%;
	}
	.two:hover {
		background-color: var(--ac4);
	}
</style>
