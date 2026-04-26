<script>
	import { page } from '$app/state';
	import { Notify } from '$lib/info';
	import { SideMenu } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';
	import { AdminNav, Footer, Header, Loading, MobileNav, Module } from './_layout/index.js';
	import './_layout/main.css';

	let { data, children } = $props();

	app.user = data.locals.user;
	app.token = data.locals.token;
	app.login = data.locals.login;
	app.likes = data.locals.likes;
	app.cart_items = data.locals.cart_items;
	app.item_all_tags = data.locals.item_all_tags;
	app.item_featured_tags = data.locals.item_featured_tags;
	app.blog_tags = data.locals.blog_tags;
	app.axis_map = data.locals.axis_map;
	app.price_map = data.locals.price_map;

	let admin_nav = $state();
</script>

<main class="{app.user.theme}_theme">
	{#if page.url.pathname.startsWith('/admin')}
		<div class="admin">
			<div class="admin_nav">
				<AdminNav onclick={() => admin_nav.onclick()}></AdminNav>
			</div>

			<div class="admin_content">
				<div class="admin_header">
					<Header />
				</div>
				{@render children()}
			</div>

			<SideMenu bind:this={admin_nav}>
				<AdminNav onclick={() => admin_nav.onclick()}></AdminNav>
			</SideMenu>
		</div>
	{:else}
		<div class="page_header">
			<Header />
		</div>

		{@render children()}

		<Footer />
		<div class="page_mobile_nav">
			<MobileNav />
		</div>
	{/if}

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

	.page_header {
		z-index: 1;
		@media screen and (min-width: 800px) {
			position: sticky;
			top: 0;
		}
	}

	.page_mobile_nav {
		position: sticky;
		bottom: 0;

		@media screen and (min-width: 800px) {
			display: none;
		}
	}

	.admin {
		display: flex;

		.admin_nav {
			display: none;
			position: sticky;
			top: 0;
			flex-shrink: 0;
			height: 100vh;
			border-right: 1px solid var(--ol);

			transition: width 0.2s ease-in-out;

			@media screen and (min-width: 600px) {
				width: 56px;
				display: block;
			}

			@media screen and (min-width: 700px) {
				width: 180px;
			}
		}

		.admin_content {
			width: 100%;
		}

		.admin_header {
			background-color: var(--bg);
		}
	}
</style>
