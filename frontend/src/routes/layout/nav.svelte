<script>
	import { page } from '$app/stores';
	import { user, module, state } from '$lib/store.js';

	import SVG from '$lib/svg.svelte';
	import Login from '../auth/login.svelte';

	$: segment = $page.url.pathname || undefined;
	let width;
</script>

<nav>
	<a href="/" class:active={segment == '/'} bind:clientWidth={width}>
		<div class="label">
			{#if segment == '/'}
				<SVG type="home_active" size="15" />
			{:else}
				<SVG type="home" size="15" />
			{/if}
			Home
		</div>
		<div class="hover" style:--height="{width}px" />
		<div class="indicator" />
	</a>
	<a href="/shop{$state.shop || ''}" class:active={segment == '/shop'}>
		<div class="label">
			{#if segment == '/shop'}
				<SVG type="shop_active" size="15" />
			{:else}
				<SVG type="shop" size="15" />
			{/if}
			Shop
		</div>
		<div class="hover" style:--height="{width}px" />
		<div class="indicator" />
	</a>
	<a href="/save{$state.save || ''}" class:active={segment == '/save'}>
		<div class="label">
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
		</div>
		<div class="hover" style:--height="{width}px" />
		<div class="indicator" />
	</a>
	<a href="/cart" class:active={segment == '/cart'}>
		<div class="label">
			{#if segment == '/cart'}
				<SVG type="cart_active" size="15" />
			{:else}
				<SVG type="cart" size="15" />
			{/if}
			Cart
			{#if $user && $user.cart.length > 0}
				{#key $user.cart}
					<div class="circle">
						{$user.cart.length}
					</div>
				{/key}
			{/if}
		</div>
		<div class="hover" style:--height="{width}px" />
		<div class="indicator" />
	</a>

	{#if $user && $user.login}
		<a href="/profile" class:active={segment == '/profile'}>
			<div class="label">
				{#if segment == '/profile'}
					<SVG type="user_active" size="15" />
				{:else}
					<SVG type="user" size="15" />
				{/if}
				User
				<div class="circle profile">✓</div>
			</div>
			<div class="hover" style:--height="{width}px" />
			<div class="indicator" />
		</a>
	{/if}

	{#if !$user?.login}
		<button
			class="login"
			on:click={() => {
				$module = {
					module: Login
				};
			}}
		>
			<div class="label">
				<SVG type="user" size="15" />
				Login
			</div>
			<div class="hover" style:--height="{width}px" />
		</button>
	{/if}
</nav>

<style>
	nav {
		display: flex;
		background-color: var(--ac6);
		box-shadow: var(--shad1);
		height: var(--headerHeight);
	}

	a,
	button {
		position: relative;

		display: flex;
		align-items: center;
		justify-content: center;

		width: 100%;
		border: none;

		background-color: transparent;
		font-size: small;
		text-decoration: none;
		cursor: pointer;
		overflow: hidden;
		transition: var(--trans1);

		color: var(--ac2);
		fill: currentColor;
	}

	.label {
		position: relative;
		z-index: 1;

		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: var(--sp0);
	}

	.hover {
		position: absolute;

		background-color: transparent;
		width: 0;
		height: 0;
		border-radius: 50%;

		transition: var(--trans1);
	}
	.indicator {
		position: absolute;
		bottom: 0;

		width: var(--sp4);
		height: 4px;
		border-radius: 10px 10px 0 0;
		background-color: transparent;

		transition: var(--trans1);
	}

	a:hover,
	.active,
	button:hover {
		color: var(--ac1);
	}
	a:hover .hover,
	button:hover .hover {
		width: 100%;
		height: var(--height);
		background-color: var(--ac5);
	}

	.active .indicator {
		background-color: var(--cl1);
	}

	.circle {
		--size: 16px;

		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		position: absolute;
		top: 0;
		right: -40%;

		width: var(--size);
		height: var(--size);

		color: var(--ac6_);

		font-size: x-small;
		border-radius: 50%;
		background-color: var(--cl1);
	}

	@media screen and (min-width: 800px) {
		nav {
			box-shadow: unset;
		}

		a,
		button {
			padding: var(--sp2);
		}

		.label {
			flex-direction: unset;
		}
		.circle {
			position: unset;
		}

		.login {
			display: none;
		}
	}
</style>
