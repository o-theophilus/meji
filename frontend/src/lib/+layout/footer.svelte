<script>
	import { page } from '$app/state';

	import Nav from './footer.nav.svelte';
	import Socials from './footer.socials.svelte';

	import { Content } from '$lib/layout';
</script>

{#if page.url.pathname != '/shop'}
	<hr />
{/if}

<Content --content-height="100%" --content-padding-top="56px" --content-padding-bottom="56px" --content-background-color="var(--bg)">
	<footer id="footer">
		<Nav />
		<br />
		<Socials />
		<div class="copyright">&copy 2026 | Meji.ng</div>
	</footer>
</Content>

<style>
	footer {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.copyright {
		margin-top: var(--sp5);
		font-size: 0.8rem;
		text-align: center;
	}
</style>
