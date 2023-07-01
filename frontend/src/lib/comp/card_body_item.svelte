<script>
	export let grid = false;
</script>

<section class:grid>
	<slot>Empty</slot>
</section>

<style>
	section {
		display: grid;
		justify-content: center;
		align-items: center;
		gap: var(--gap2);
		grid-template-columns: 1fr;

		color: var(--font1);

		padding: var(--gap2);
		border-top: 2px solid var(--background);
	}
	.grid {
		grid-template-columns: repeat(2, 1fr);
	}
	@media screen and (min-width: 700px) {
		.grid {
			grid-template-columns: repeat(3, 1fr);
		}
	}
	@media screen and (min-width: 1000px) {
		.grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}
</style>
