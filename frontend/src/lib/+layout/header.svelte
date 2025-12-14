<script>
	import { page } from '$app/state';
	import { app, module } from '$lib/store.svelte.js';

	import { Icon } from '$lib/macro';
	import { Login } from '$lib/auth';
	import Link from './nav.btn.svelte';
	import Theme from './header.theme.svelte';
	import Notification from './header.notification.svelte';
	import User from './header.user.svelte';
</script>

<div class="block">
	<a href="/">
		<Icon icon="logo" size="32" />
		Meji
	</a>
	<div class="line">
		<Notification />
		<Theme />
		{#if app.login}
			<User />
		{/if}
	</div>
</div>

<style>
	.block {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--sp2);
		flex-wrap: wrap;

		min-height: var(--headerHeight);
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		padding: 16px 24px;
	}

	a {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		color: var(--ft1);
		fill: var(--cl1);
		font-weight: 800;
		text-decoration: none;

		transition: color var(--trans);
	}

	.line {
		gap: 16px;
	}
</style>
