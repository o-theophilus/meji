<script>
	import Center from './center.svelte';
</script>

<Center>
	<div class="card">
		<slot />
	</div>
</Center>

<style>
	.card {
		width: 100%;
		padding: var(--sp3);
		border-radius: var(--sp0);

		color: var(--ac2);
		background-color: var(--ac6);
		box-shadow: var(--shad1);
	}

	@media screen and (min-width: 700px) {
		.card {
			padding: calc(var(--sp5) - var(--sp2)) var(--sp5);
		}
	}
</style>
