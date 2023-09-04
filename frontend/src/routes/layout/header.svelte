<script>
	import SVG from '$lib/comp/svg.svelte';
	import Theme from './header.theme.svelte';
	import Nav from './nav.svelte';
	import Auth from './header.auth.svelte';
</script>

<header>
	<div class="block">
		<a href="/">
			<SVG type="logo" size="40" />
			<h1>Meji</h1>
		</a>
		<div class="right">
			<Theme />
			<div class="nav">
				<Nav />
			</div>
			<Auth />
		</div>
	</div>
</header>

<style>
	header {
		background-color: var(--ac5);
		box-shadow: var(--shad1);
	}
	.block {
		display: flex;
		align-items: center;
		justify-content: space-between;

		width: min(100%, 1200px);
		height: var(--headerHeight);
		padding: 0 var(--sp2);

		margin: auto;
	}

	a {
		flex-shrink: 0;

		display: flex;
		align-items: center;
		gap: var(--sp2);

		height: calc(var(--headerHeight) - var(--sp2));

		color: var(--ac1);
		fill: var(--cl1);
		text-decoration: none;
	}

	.right {
		display: flex;
		align-items: center;
	}
	.nav {
		display: none;
		height: 100%;
	}

	@media screen and (min-width: 800px) {
		.nav {
			display: unset;
		}
	}
</style>
