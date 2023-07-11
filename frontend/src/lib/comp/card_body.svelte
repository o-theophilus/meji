<script>
</script>

<section class="body">
	<slot>No Item</slot>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		color: var(--ac1);

		padding: var(--sp2);
	}
	.body:not(:first-child) {
		border-top: 2px solid var(--ac5);
	}
</style>
