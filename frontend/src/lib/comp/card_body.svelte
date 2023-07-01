<script>
</script>

<section class="body">
	<slot>No Item</slot>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap2);

		color: var(--font1);

		padding: var(--gap2);
	}
	.body:not(:first-child) {
		border-top: 2px solid var(--background);
	}
</style>
