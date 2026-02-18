<script>
	import { page } from '$app/state';
	import { Login } from '$lib/auth';
	import { Avatar, Icon } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import { quadIn } from 'svelte/easing';
	import { scale } from 'svelte/transition';

	const buttons = $derived([
		{ name: 'Home', icon: 'home', href: '/' },
		{ name: 'Shop', icon: 'shop', href: '/shop' },
		{ name: 'Save', icon: 'bookmark', href: '/save', count: app.likes.length },
		{ name: 'Cart', icon: 'cart', href: '/cart', count: app.cart_items.length }
	]);
</script>

<div class="bottom_nav">
	<div class="block">
		{#each buttons as x}
			{@const active = x.href.split('/')[1] == page.url.pathname.split('/')[1]}
			<a class:active href={x.href} data-sveltekit-preload-data>
				<div class="center">
					<Icon icon={!active ? x.icon : `${x.icon}_active`} size="16" />
					{x.name}

					{#if x.count > 0}
						{#key x.count}
							<div class="count" in:scale={{ easing: quadIn }}>
								{x.count}
							</div>
						{/key}
					{/if}
				</div>
			</a>
		{/each}

		{#if app.login}
			<a
				class:active={`@${app.user.username}` == page.url.pathname.split('/')[1]}
				href="/@{app.user.username}"
				data-sveltekit-preload-data
			>
				<div class="center">
					<Avatar
						name={app.user.name}
						photo={app.user.photo}
						size="20"
						--avatar-border-radius="40%"
					/>
					Profile
				</div>
			</a>
		{:else}
			<button onclick={() => module.open(Login)}>
				<div class="center">
					<Icon icon="user" size="16" />
					Login
				</div>
			</button>
		{/if}
	</div>
</div>

<style>
	.bottom_nav {
		background-color: var(--bg);
		border-top: 1px solid var(--ol);

		& .block {
			display: flex;
			align-items: center;

			max-width: var(--mobileWidth);
			height: var(--headerHeight2);
			margin: auto;
		}

		position: relative;

		&::before {
			content: '';
			position-anchor: --active;

			position: absolute;
			top: anchor(top);
			right: anchor(right);
			left: anchor(left);
			height: 4px;

			background-color: var(--cl1);
			border-radius: var(--toggle-border-radius, 4px);

			transition:
				right 0.2s ease-in-out,
				left 0.2s ease-in-out;
		}
	}

	button {
		all: unset;
		cursor: pointer;
	}

	button,
	a {
		display: flex;
		align-items: center;
		justify-content: center;

		width: 100%;
		height: 100%;
		border-radius: 8px;

		text-decoration: none;

		transition: background-color 0.2s ease-in-out;

		&.active {
			anchor-name: --active;
			background-color: var(--bg2);

			& .center {
				color: var(--ft1);
				fill: var(--ft1);
				font-weight: 600;
			}
		}

		/* &:hover { */
			/* background-color: var(--bg1); */
		/* } */

		& .center {
			position: relative;

			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			gap: 4px;

			color: var(--ft2);
			fill: var(--ft2);
			font-size: 0.7rem;
			line-height: 100%;

			@media screen and (min-width: 580px) {
				& {
					font-size: 0.8rem;
				}
			}

			transition:
				color 0.2s ease-in-out,
				fill 0.2s ease-in-out,
				font-weight 0.2s ease-in-out;
		}
	}

	.count {
		position: absolute;
		top: -3px;
		right: -5px;

		display: flex;
		align-items: center;
		justify-content: center;

		width: 12px;
		height: 12px;
		border-radius: 50%;

		font-size: 0.6rem;
		background-color: var(--cl1);
		color: white;
	}
</style>
