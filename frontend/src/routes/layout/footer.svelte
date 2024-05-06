<script>
	import Nav from './footer.nav.svelte';
	import Contact from './footer.contact.svelte';
	import Copy from './footer.copy.svelte';
	import Social from './footer.social.svelte';
	import Center from '$lib/center.svelte';
</script>

<footer>
	<Center>
		<Nav />
		<br />
		<br />
		<Contact />
		<br />
		<Social />
		<br />
		<br />
		<div class="row">
			<Copy />
		</div>
	</Center>
</footer>

<style>
	footer {
		padding-bottom: var(--sp5);
	}

	.row {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	@media screen and (min-width: 800px) {
	}
</style>
