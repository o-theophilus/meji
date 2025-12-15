<script>
	import '$lib/+layout/var.css';
	import '$lib/+layout/main.css';
	import { app } from '$lib/store.svelte.js';
	import { Header, Nav, Footer, Module, Loading } from '$lib/+layout';
	import { Notify } from '$lib/info';

	let { data, children } = $props();
	app.user = data.locals.user;
	app.token = data.locals.token;
	app.login = data.locals.login;
	app.likes = data.locals.likes;
	app.cart_items = data.locals.cart_items;
</script>

<main class:dark={app.user.theme == 'dark'}>
	<Header />
	<!-- <Nav /> -->
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

		background-color: var(--bg1);
		color: var(--ft2);
		transition:
			background-color var(--trans),
			color var(--trans);
	}

	.nav {
		position: sticky;
		bottom: 0;
	}

	/* @media screen and (min-width: 800px) {
		.nav {
			display: none;
		}
	} */
</style>
