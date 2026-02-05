<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { page } from '$app/state';
	import { app, module } from '$lib/store.svelte.js';
	import { Avatar } from '$lib/macro';
	import { Logout, Login } from '$lib/auth';
	import { Hamburger, Button } from '$lib/button';
	import Theme from './header.menu.theme.svelte';

	let menu = $state();
	let open = $state(false);
	let can_close = $state(false);

	let trim = (name, length) => {
		let temp = name.split(' ')[0];
		return temp.length > length ? `${temp.slice(0, length - 3)}...` : temp;
	};
</script>

<svelte:window
	onclick={(e) => {
		if (menu && menu.contains(e.target)) return;
		if (open && !can_close) open = false;
		can_close = false;
	}}
/>

<section>
	<Hamburger
		--hamburger-background-color="transpatent"
		--hamburger-background-color-hover="var(--bg1)"
		--hamburger-color="var(--ft2)"
		--hamburger-color-hover="var(--ft1)"
		{open}
		onclick={() => {
			open = !open;
			can_close = true;
		}}
	></Hamburger>

	{#if open}
		<div
			bind:this={menu}
			class="menu"
			transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}
			role="presentation"
		>
			{#if app.login}
				<a
					href="/@{app.user.username}"
					class="menu_item profile"
					onclick={() => {
						open = false;
						can_close = false;
					}}
				>
					<Avatar
						name={app.user.name}
						photo={app.user.photo}
						size="32"
						--avatar-border-radius="40%"
					/>
					<div class="details" title="{app.user.email}">
						<div class="name">
							{trim(app.user.name, 20)}
						</div>
						<div class="email">
							{trim(app.user.email, 40)}
						</div>
					</div>
				</a>
				<a
					href="/orders"
					class="menu_item"
					onclick={() => {
						open = false;
						can_close = false;
					}}>Orders</a
				>
				<a
					href="/admin"
					class="menu_item"
					onclick={() => {
						open = false;
						can_close = false;
					}}>Admin</a
				>
				{#if app.user.access.includes('log:view')}
					<a
						href="/log"
						class="menu_item"
						onclick={() => {
							open = false;
							can_close = false;
						}}>Logs</a
					>
				{/if}
			{/if}
			<div class="menu_item theme">
				Theme
				<Theme />
			</div>
			<div class="menu_item logout">
				{#if app.login}
					<Logout />
				{:else}
					<Button
						icon="log-in"
						--button-height="40px"
						--button-font-size="0.8rem"
						onclick={() => module.open(Login)}
					>
						Login
					</Button>
				{/if}
			</div>
		</div>
	{/if}
</section>

<style>
	section {
		position: relative;
	}

	.menu {
		position: absolute;
		top: 40px;
		right: 0;
		z-index: 1;

		width: max-content;
		display: flex;
		flex-direction: column;
		background-color: var(--bg3);
		border-radius: 4px;
		outline: 1px solid var(--ol);
		outline-offset: -1px;
	}

	.menu_item {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;

		color: var(--ft2);
		font-size: 0.8rem;
		padding: 8px;
		background-color: transparent;
		border-top: 1px solid var(--ol);
	}

	a {
		text-decoration: none;
		transition:
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out;

		&:hover {
			background-color: var(--bg2);
			color: var(--ft1);
		}
	}

	.profile {
		border: none;
		padding: 16px;

		& .name {
			font-weight: 600;
		}
		& .email {
			font-size: 0.7rem;
		}
	}

	.theme,
	.logout {
		padding: 16px;
	}
</style>
