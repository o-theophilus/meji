<script>
	import './layout.var.css';
	import './layout.main.css';
	import './layout.form.css';

	// import { onMount } from 'svelte';

	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Header from './layout.header.svelte';
	import Footer from '$lib/footer/index.svelte';
	import Nav from './layout.nav.svelte';

	import Module from '$lib/module/module.svelte';
	import Loading from '$lib/comp/loading.svelte';

	export let data;
	$user = data.locals.user;
	$token = data.locals.token;

	let innerWidth;
	let scrollY;
</script>

<svelte:window bind:innerWidth bind:scrollY />

<main class:dark={$user.setting.theme == 'dark'} id="top">
	<Header />
	<div class="page">
		<slot />
	</div>
	<Footer />
	<div class="nav">
		<Nav />
	</div>

	<Module />
	<Loading />
</main>

<style>
	main {
		position: relative;
		/* background: var(--background); */
		background: var(--foreground);
	}

	.page {
		width: min(100%, 1200px);
		min-height: calc(100vh - var(--headerHeight) * 2);

		margin: auto;
		padding: var(--gap1);
		padding-top: 0;
	}
	.nav {
		position: sticky;
		bottom: 0;
	}
	@media screen and (min-width: 800px) {
		.page {
			min-height: calc(100vh - var(--headerHeight));
		}
		.nav {
			display: none;
		}
	}
</style>
