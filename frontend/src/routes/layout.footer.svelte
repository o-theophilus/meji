<script>
	import Nav from './layout.footer.nav.svelte';
	import Copy from './layout.footer.copy.svelte';
</script>

<footer>
	<Nav />
	<Copy />
	<br />
	<br />
</footer>

<style>
	footer {
		color: var(--ac1);

		display: flex;
		flex-direction: column;
		gap: var(--sp1);

		width: 100%;
		max-width: 800px;

		padding: var(--sp3) var(--sp2);

		margin: auto;
	}

	@media screen and (min-width: 800px) {
	}
</style>
