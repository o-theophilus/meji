<script>
	import { page } from '$app/stores';
	import { user, module, state } from '$lib/store.js';

	import SVG from '$lib/svg.svelte';
	import Login from '../auth/login.svelte';

	$: segment = $page.url.pathname || undefined;
</script>

<nav>
	<a href="/" class:active={segment == '/'}>
		{#if segment == '/'}
			<SVG type="home_active" size="15" />
		{:else}
			<SVG type="home" size="15" />
		{/if}
		Home
		<div class="indicator" />
	</a>
	<a href="/shop{$state.shop || ''}" class:active={segment == '/shop'}>
		{#if segment == '/shop'}
			<SVG type="shop_active" size="15" />
		{:else}
			<SVG type="shop" size="15" />
		{/if}
		Shop
		<div class="indicator" />
	</a>
	<a href="/save{$state.save || ''}" class:active={segment == '/save'}>
		{#if segment == '/save'}
			<SVG type="like_active" size="15" />
		{:else}
			<SVG type="like" size="15" />
		{/if}
		Save
		{#if $user && $user.saves.length > 0}
			{#key $user.saves.length}
				<div class="circle">
					{$user.saves.length}
				</div>
			{/key}
		{/if}

		<div class="indicator" />
	</a>
	<a href="/cart" class:active={segment == '/cart'}>
		{#if segment == '/cart'}
			<SVG type="cart_active" size="15" />
		{:else}
			<SVG type="cart" size="15" />
		{/if}
		Cart
		{#if $user && $user.cart.length > 0}
			{#key $user.cart.length}
				<div class="circle">
					{$user.cart.length}
				</div>
			{/key}
		{/if}
		<div class="indicator" />
	</a>

	{#if $user && $user.login}
		<a href="/profile" class:active={segment == '/profile'}>
			{#if segment == '/profile'}
				<SVG type="user_active" size="15" />
			{:else}
				<SVG type="user" size="15" />
			{/if}
			User
			<div class="circle profile">✓</div>
			<div class="indicator" />
		</a>
	{:else}
		<button
			on:click={() => {
				$module = {
					module: Login,
					data: {
						return_url: $page.url.pathname
					}
				};
			}}
		>
			<SVG type="user" size="15" />
			Login
		</button>
	{/if}
</nav>

<style>
	nav {
		display: flex;
		background-color: var(--ac5);
		box-shadow: var(--shad1);
		height: var(--headerHeight);
	}

	a,
	button {
		position: relative;

		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 4px;

		width: 100%;
		border: none;
		background-color: transparent;
		color: var(--ac1);
		fill: currentColor;

		font-size: small;
		text-decoration: none;
		cursor: pointer;

		transition: var(--trans1);
	}
	.indicator {
		position: absolute;
		bottom: 0;

		width: 100%;
		height: 6px;
		border-radius: 10px 10px 0 0;
		background-color: transparent;

		transition: var(--trans1);
	}

	a:hover,
	button:hover,
	.active {
		color: var(--cl1);
	}
	.active .indicator {
		background-color: var(--cl1);
	}

	.circle {
		--size: 16px;

		display: flex;
		align-items: center;
		justify-content: center;

		position: absolute;
		top: 5px;
		right: calc(50% - (var(--size) * 1.4));

		width: var(--size);
		height: var(--size);

		color: var(--ac5_);

		font-size: x-small;
		border-radius: 50%;
		background-color: var(--cl1);
	}

	@media screen and (min-width: 800px) {
		nav {
			box-shadow: unset;
		}

		button,
		a {
			flex-direction: unset;
			padding: var(--sp2);
		}
		.circle {
			position: unset;
		}
	}
</style>
