<script>
	import SVG from '$lib/svg.svelte';

	export let form;
</script>

<section>
	{#each Array(5) as _, i}
		<button
			class:active={5 - i == form.rating}
			on:click={() => {
				form.rating = 5 - i;
			}}
		>
			<SVG type="star" size="24" />
		</button>
	{/each}
</section>

<style>
	section {
		display: flex;
		flex-direction: row-reverse;
		width: fit-content;
	}
	button {
		display: flex;
		align-items: center;

		cursor: pointer;
		border: none;
		padding: 0 var(--sp0);
		background-color: transparent;
	}
	button:first-child {
		padding-right: 0;
	}
	button:last-child {
		padding-left: 0;
	}

	button.active {
		fill: var(--cl6);
	}
	button.active ~ button {
		fill: var(--cl6);
	}

	button:hover {
		fill: gold !important;
	}
	button:hover ~ button {
		fill: gold;
	}
</style>
