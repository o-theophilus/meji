<script>
	import Nav from './layout.footer.nav.svelte';
	import Copy from './layout.footer.copy.svelte';
</script>

<footer>
	<Nav />
	<Copy />
</footer>



<style>
	footer {
		color: var(--font1);

		display: flex;
		flex-direction: column;
		gap: var(--gap1);

		width: 100%;
		max-width: 800px;

		padding: var(--gap3) var(--gap2);

		margin: auto;
	}

	@media screen and (min-width: 800px) {
	}
</style>
