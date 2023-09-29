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
		margin-top: var(--sp2);
		border-radius: var(--sp0);

		color: var(--ac1);
		background-color: var(--ac5);
		box-shadow: var(--shad1);
	}

	@media screen and (min-width: 700px) {
		.card {
			padding: var(--sp5);
		}
	}
</style>
