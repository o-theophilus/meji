<script>
	import SVG from '$lib/comp/svg.svelte';

	export let id;
	export let value = 0;

	export let width = 0;
</script>

<section>
	<div class="left">
		{id}
		<div class="svg">
			<SVG type="star" size="12" />
		</div>
		({value})
	</div>
	<div class="bar">
		<div class="fill" style="width: {width}%;" />
	</div>
</section>

<style>
	section {
		display: flex;

		gap: var(--sp2);
		align-items: center;
	}
	.left {
		display: flex;
		align-items: center;
		justify-content: space-between;

		width: 100px;
	}
	.svg {
		display: flex;
		align-items: center;
		justify-content: center;

		fill: var(--cl6);
	}
	.bar {
		/* display: flex; */

		height: 20px;
		width: 100%;

		border: 2px solid var(--ac5);
		border-radius: var(--brad1);

		overflow: hidden;
	}
	.fill {
		height: 100%;

		background: var(--cl6);
	}
</style>
