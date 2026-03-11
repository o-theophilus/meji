<script>
	import { Button } from '$lib/button';
	import { Header } from '../_layout/index.js';
	import Nav from './nav.svelte';

	let { children } = $props();

	let ops = $state({ open: false });
	let menu = $state();
	let can_close = $state(false);
</script>

<svelte:window
	onresize={(e) => {
		if (e.target.innerWidth > 600) {
			ops.open = false;
		}
	}}
	onclick={(e) => {
		if (menu && menu.contains(e.target)) return;
		if (ops.open && !can_close) ops.open = false;
		can_close = false;
	}}
/>

<div class="container">
	<div class="nav">
		<Nav bind:ops side_bar></Nav>
	</div>

	<div class="open_nav">
		<Button
			icon="panel-left-open"
			onclick={() => {
				ops.open = !ops.open;
				can_close = true;
			}}
		></Button>
	</div>

	<div class="nav_mobile" bind:this={menu} class:open={ops.open}>
		<Nav bind:ops wide></Nav>
	</div>

	<div class="page">
		<Header />
		{@render children()}
	</div>
</div>

<style>
	.container {
		display: flex;
		background-color: var(--bg1);
	}
	.nav {
		display: none;
		position: sticky;
		flex-shrink: 0;
		top: 0;

		width: 64px;

		transition: width 0.2s ease-in-out;

		@media screen and (min-width: 700px) {
			width: 180px;
		}

		height: 100vh;
		padding: 8px;
		padding-right: 0;
	}

	.nav_mobile {
		position: fixed;
		bottom: -300px;
		left: 0;
		right: 0;
		z-index: 1;

		border-top: 1px solid var(--ol);
		height: 300px;
		transition: bottom 0.2s ease-in-out;

		&.open {
			bottom: 0;
		}
	}

	.open_nav {
		padding: 16px;
		position: fixed;
		bottom: 0;
		left: 0;
		z-index: 1;
		--button-width: 40px;
		--button-height: 40px;
	}

	@media screen and (min-width: 600px) {
		.nav {
			display: block;
		}
		.open_nav,
		.nav_mobile {
			display: none;
		}
	}

	.page {
		width: 100%;
	}
</style>
