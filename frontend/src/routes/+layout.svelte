<script>
	import { Notify } from '$lib/info';
	import { app } from '$lib/store.svelte.js';
	import { Footer, Header, Loading, Module, Nav } from './_layout/index.js';
	import './_layout/main.css';

	let { data, children } = $props();
	app.user = data.locals.user;
	app.token = data.locals.token;
	app.login = data.locals.login;
	app.likes = data.locals.likes;
	app.cart_items = data.locals.cart_items;
	app.tags = data.locals.tags;
</script>

<main class="{app.user.theme}_theme">
	<Header />
	{@render children()}
	<Footer />

	<div class="nav">
		<Nav />
	</div>

	<Module />
	<Loading />
	<Notify />
</main>

<style>
	main {
		position: relative;

		background-color: var(--bg);
		color: var(--ft2);
		transition:
			background-color 0.2s ease-in-out,
			color 0.2s ease-in-out;
	}

	.nav {
		position: sticky;
		bottom: 0;
	}
</style>
