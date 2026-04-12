<script>
	import { Button, Hamburger } from '$lib/button';
	import { Avatar } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';
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
					<div class="details" title={app.user.email}>
						<div class="name">
							{trim(app.user.name, 20)}
						</div>
						<div class="email">
							{trim(app.user.email, 40)}
						</div>
					</div>
				</a>
			{/if}

			<a
				href="/about"
				class="menu_item hide"
				onclick={() => {
					open = false;
					can_close = false;
				}}>About</a
			>
			<a
				href="/partner"
				class="menu_item hide"
				onclick={() => {
					open = false;
					can_close = false;
				}}>Partner</a
			>
			<a
				href="/blog"
				class="menu_item hide"
				onclick={() => {
					open = false;
					can_close = false;
				}}>Blog</a
			>
			<a
				href="/contact"
				class="menu_item hide"
				onclick={() => {
					open = false;
					can_close = false;
				}}>Contact Us</a
			>

			{#if app.login}
				{#if app.user.access.length}
					<a
						href="/admin"
						class="menu_item"
						onclick={() => {
							open = false;
							can_close = false;
						}}
					>
						Admin
					</a>
				{/if}
				<a
					href="/orders"
					class="menu_item"
					onclick={() => {
						open = false;
						can_close = false;
					}}>Orders</a
				>
				{#if app.user.access.includes('log.view')}
					<a
						href="/log"
						class="menu_item"
						onclick={() => {
							open = false;
							can_close = false;
						}}
					>
						Logs
					</a>
				{/if}
			{/if}
			<div class="menu_item theme">
				Theme
				<Theme />
			</div>
			{#if app.login}
				<div class="menu_item logout">
					<Button
						icon="log-out"
						--button-height="40px"
						--button-font-size="0.8rem"
						--button-background-color-hover="red"
						onclick={async () => {
							open = false;
							can_close = false;

							let resp = await fetch(`${import.meta.env.VITE_BACKEND}/logout`, {
								method: 'delete',
								headers: {
									'Content-Type': 'application/json',
									Authorization: app.token
								}
							});

							resp = await resp.json();

							if (resp.status == 200) {
								app.token = resp.token;
								app.login = false;
								document.location = '/';
							}
						}}
					>
						Logout
					</Button>
				</div>
			{/if}
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

		@media screen and (min-width: 580px) {
			&.hide {
				display: none;
			}
		}
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
