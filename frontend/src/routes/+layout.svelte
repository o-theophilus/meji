<script>
	import './layout/var.css';
	import './layout/main.css';

	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Header from './layout/header.svelte';
	import Footer from './layout/footer.svelte';
	import Nav from './layout/nav.svelte';
	import Module from './layout/module.svelte';
	import Toast from './layout/toast.svelte';
	import Loading from './layout/loading.svelte';

	export let data;
	$user = data.locals.user;
	$token = data.locals.token;

	let innerWidth;
	let scrollY;
</script>

<svelte:window bind:innerWidth bind:scrollY />

<main class:dark={$user.setting_theme == 'dark'} id="top">
	<Header />
	<div class="page">
		<slot />
	</div>
	<Footer />
	<div class="nav">
		<Nav />
	</div>

	<Module />
	<div class="toast">
		<Toast />
	</div>
	<Loading />
</main>

<style>
	main {
		position: relative;
		background: var(--ac5);
	}

	.page {
		min-height: calc(100vh - var(--headerHeight) * 2);
		
		
	}
	.nav {
		position: sticky;
		bottom: 0;
	}
	.toast {
		position: fixed;
		right: var(--sp2);
		top: calc(var(--headerHeight) + var(--sp2));
		z-index: 1;
	}
	@media screen and (min-width: 800px) {
		.page {
			min-height: calc(100vh - var(--headerHeight));
		}
		.nav {
			display: none;
		}
		/* .toast {
			bottom: var(--sp2);
		} */
	}
</style>
