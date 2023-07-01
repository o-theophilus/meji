<script>
	import SVG from '$lib/comp/svg.svelte';
	import Theme from './layout.header.theme.svelte';
	import Nav from './layout.nav.svelte';
	import Auth from './layout.header.auth.svelte';
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
		background-color: var(--foreground);
		box-shadow: var(--shad1);
	}
	.block {
		display: flex;
		align-items: center;
		justify-content: space-between;

		width: min(100%, 1200px);
		height: var(--headerHeight);
		padding: 0 var(--gap1);

		margin: auto;
	}

	a {
		flex-shrink: 0;

		display: flex;
		align-items: center;
		gap: var(--gap2);

		height: calc(var(--headerHeight) - var(--gap2));

		color: var(--font1);
		fill: var(--color1);
		text-decoration: none;
	}

	.right {
		display: flex;
		align-items: center;
		/* gap: var(--gap2); */
	}
	.nav {
		display: none;
		height: 100%;
	}

	@media screen and (min-width: 800px) {
		.block {
			padding: 0 var(--gap3);
		}
		.nav {
			display: unset;
		}
	}
</style>
