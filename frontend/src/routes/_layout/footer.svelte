<script>
	import { page } from '$app/state';

	import Nav from './footer.nav.svelte';
	import Socials from './footer.socials.svelte';

	import { Content } from '$lib/layout';
	import { Icon } from '$lib/macro';
</script>

{#if page.url.pathname != '/shop'}
	<hr />
{/if}

<Content
	--content-height="100%"
	--content-padding-top="56px"
	--content-padding-bottom="56px"
	--content-background-color="var(--bg)"
>
	<footer id="footer">
		<div class="left">
			<div class="logo">
				<a href="/">
					<Icon icon="logo" size="32" />
					Meji
				</a>
				<span class="copyright"> Your best online shopping experince </span>
			</div>
			<Socials />
		</div>

		<Nav />
	</footer>

	<div class="copyright">&copy 2026 | Meji.ng</div>
</Content>

<style>
	footer {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 40px;
	}

	@media screen and (min-width: 600px) {
		footer {
			flex-direction: unset;
		}
	}

	.left {
		& .logo {
			margin-bottom: 16px;
		}

		& a {
			display: flex;
			align-items: center;
			gap: 8px;

			width: fit-content;
			color: var(--ft1);
			fill: var(--cl1);
			font-weight: 800;
			text-decoration: none;

			transition: color 0.2s ease-in-out;
		}
	}

	.copyright {
		margin-top: 80px;
		font-size: 0.7rem;
		text-align: center;
	}
</style>
