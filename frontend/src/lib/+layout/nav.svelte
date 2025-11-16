<script>
	import { app, module } from '$lib/store.svelte.js';

	import { Icon } from '$lib/macro';
	import { Login } from '$lib/auth';
	import Link from './nav.btn.svelte';
	import User from './nav.user.svelte';
</script>

<div class="block">
	<Link name="Home" icon="home" href="/"></Link>
	<Link name="Shop" icon="shop" href="/shop"></Link>
	<Link name="Save" icon="save" href="/save"></Link>
	<Link name="Cart" icon="cart" href="/cart"></Link>
	{#if app.login}
		<Link name="User" icon="user" href="/@{app.user.username}"></Link>
		<!-- <User /> -->
	{:else}
		<Link name="Login" icon="user" onclick={() => module.open(Login)}></Link>
	{/if}
</div>

<style>
	.block {
		display: flex;
		align-items: center;

		/* min-height: var(--headerHeight); */
		max-width: var(--mobileWidth);
		width: 100%;
		margin: auto;
		/* padding: var(--sp2); */

		background-color: var(--bg1);
	}
</style>
