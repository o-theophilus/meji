<script>
	import { page } from '$app/stores';
	import Contact from './footer.contact.svelte';
</script>

<footer>
	{#if $page.url.pathname == '/'}
		<Contact />
	{/if}

	<br />
	<br />
	<div class="nav">
		<a href="/">Home</a>
		&#8226; <a href="/#about">About</a>
		<!-- &#8226; <a href="/terms">Terms</a> -->
	</div>

	<br />
	<div class="copyright">&copy; Meji.ng 2021</div>

	<br />
	<br />
</footer>

<style>
	footer {
		color: var(--ac1);

		width: min(100%, 1200px);

		margin: auto;
		padding: 0 var(--sp2);
	}

	@media screen and (min-width: 800px) {
	}

	.nav {
		text-align: center;
	}

	a {
		color: var(--ac1);
		text-decoration: none;

		border-bottom: 2px solid transparent;
	}
	a:hover {
		border-color: var(--cl1);
	}

	.copyright {
		text-align: center;
		font-size: small;
	}
</style>
