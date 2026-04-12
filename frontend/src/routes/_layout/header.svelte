<script>
	import { Login } from '$lib/auth';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import Menu from './header.menu.svelte';
	import Nav from './header.nav.svelte';

	let trim = (name, length) => {
		let temp = name.split(' ')[0];
		return temp.length > length ? `${temp.slice(0, length - 3)}...` : temp;
	};
</script>

<section id="page_top">
	<div class="block">
		<a href="/">
			<Icon icon="logo" size="32" />
			Meji
		</a>
		<Nav></Nav>
		<div class="right">
			{#if !app.login}
				<Button
					icon="log-in"
					--button-height="40px"
					--button-font-size="0.8rem"
					onclick={() => module.open(Login)}
				>
					Login
				</Button>
			{/if}
			<Menu></Menu>
		</div>
	</div>
</section>

<style>
	section {
		border-bottom: 1px solid var(--ol);
		background-color: var(--bg);
	}

	.block {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 16px;

		min-height: var(--headerHeight);
		max-width: var(--pageWidth);
		width: 100%;
		margin: auto;
		padding: 0 16px;

		@media screen and (min-width: 580px) {
			padding: 0 24px;
		}

		.right {
			display: flex;
			gap: 8px;
		}
	}

	a {
		display: flex;
		align-items: center;
		gap: 8px;

		color: var(--ft1);
		fill: var(--cl1);
		font-weight: 800;
		text-decoration: none;

		transition: color 0.2s ease-in-out;
	}
</style>
