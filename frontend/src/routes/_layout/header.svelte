<script>
	import { page } from '$app/state';
	import { app, module } from '$lib/store.svelte.js';
	import { Icon } from '$lib/macro';
	import { Login } from '$lib/auth';
	import Menu from './header.menu.svelte';
	import Link from './nav.btn.svelte';

	import Notification from './header.notification.svelte';

	let trim = (name, length) => {
		let temp = name.split(' ')[0];
		return temp.length > length ? `${temp.slice(0, length - 3)}...` : temp;
	};
</script>

<section>
	<div class="block">
		<a href="/">
			<Icon icon="logo" size="32" />
			Meji
		</a>
		<div class="line">
			<Notification />
			{#if app.login}
				<div class="name">
					Hello, {trim(app.user.name, 20)}
				</div>
			{/if}
			<Menu></Menu>
		</div>
	</div>
</section>

<style>
	section {
		border-bottom: 1px solid var(--ol);
	}

	.block {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 16px;
		flex-wrap: wrap;

		min-height: var(--headerHeight);
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 16px;

		@media screen and (min-width: 580px) {
			& {
				padding-left: 24px;
				padding-right: 24px;
			}
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

	.line {
		gap: 16px;
	}

	.name {
		font-size: 0.8rem;
	}
</style>
