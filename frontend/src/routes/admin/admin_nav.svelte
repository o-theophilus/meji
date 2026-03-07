<script>
	import { page } from '$app/state';
	import { Icon } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';

	let { ops = $bindable() } = $props();
	const buttons = [
		{
			name: 'Dashboard',
			href: '/admin',
			access: null,
			icon: 'layout-dashboard'
		},
		{
			name: 'Admin',
			href: '/admin/users_admin',
			access: 'user:set_access',
			icon: 'shield-check'
		},
		{
			name: 'Users',
			href: '/admin/users',
			access: 'user:view',
			icon: 'users'
		},
		{
			name: 'Reports',
			href: '/admin/report',
			access: 'report:view',
			icon: 'flag-triangle-right'
		},
		{
			name: 'Blocked Users',
			href: '/admin/block',
			access: 'block:view',
			icon: 'user-x'
		},
		{
			name: 'File Error',
			href: '/admin/file_error',
			access: 'admin:manage_files',
			icon: 'file-warning'
		},
		{
			name: 'Adverts',
			href: '/admin/advert',
			access: 'item:advert',
			icon: 'megaphone'
		},
		{
			name: 'Coupons',
			href: '/admin/coupons',
			access: 'coupon:view',
			icon: 'ticket-percent'
		},
		{
			name: 'Maintenance',
			href: '/admin/maintenance',
			access: 'admin:maintenance',
			icon: 'wrench'
		}
	];

	const buttons2 = [
		{
			name: 'Orders',
			href: '/orders',
			access: 'order:view',
			icon: 'shopping-cart',
			icon2: 'arrow-up-right'
		},
		{
			name: 'Log',
			href: '/log',
			access: 'log:view',
			icon: 'clipboard-list',
			icon2: 'arrow-up-right'
		},
		{
			name: 'Collapse',
			onclick: () => (ops.open = !ops.open),
			access: null,
			icon: 'clipboard-list'
		}
	];
</script>

<div class="nav">
	<div class="block" class:small={!ops.open}>
		<div class="top">
			{#each buttons as x}
				{@const a = x.href.split('/')}
				{@const b = page.url.pathname.split('/')}
				{@const active = a[a.length - 1] == b[b.length - 1]}

				{#if app.user.access.includes(x.access) || x.access === null}
					<a class:active href={x.href} data-sveltekit-preload-data>
						<Icon icon={x.icon}></Icon>
						<div class="name">
							{x.name}

							{#if x.icon2}
								<Icon icon={x.icon2}></Icon>
							{/if}
						</div>
					</a>
				{/if}
			{/each}
		</div>

		<div class="bottom">
			{#each buttons2 as x}
				{#if app.user.access.includes(x.access) || x.access === null}
					{#if x.href}
						<a href={x.href} data-sveltekit-preload-data>
							<Icon icon={x.icon}></Icon>
							<div class="name">
								{x.name}

								{#if x.icon2}
									<Icon icon={x.icon2}></Icon>
								{/if}
							</div>
						</a>
					{:else}
						<button onclick={() => (ops.open = !ops.open)}>
							{#key ops.open}
								<Icon icon={ops.open ? 'panel-left-close' : 'panel-left-open'}></Icon>
							{/key}
							<div class="name">Collapse</div>
						</button>
					{/if}
				{/if}
			{/each}
		</div>
	</div>
</div>

<style>
	.nav {
		position: sticky;
		top: 0;
		bottom: var(--headerHeight2);

		padding: 8px;
		align-self: flex-start;
		height: calc(100vh - var(--headerHeight) - var(--headerHeight2));
	}

	.block {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		flex-shrink: 0;
		padding: 8px;
		height: 100%;
		background-color: var(--bg);
		border-radius: 8px;

		position: relative;

		&::before {
			content: '';
			position-anchor: --active;

			position: absolute;
			top: anchor(top);
			right: anchor(right);
			bottom: anchor(bottom);
			width: 4px;

			background-color: var(--cl1);
			border-radius: var(--toggle-border-radius, 4px);

			transition:
				top 0.2s ease-in-out,
				bottom 0.2s ease-in-out;
		}

		&.small {
			& a,
			& button {
				padding: 0;
				width: 40px;

				& .name {
					display: none;
				}
			}
		}

		& button {
			all: unset;
			cursor: pointer;
			box-sizing: border-box;
		}

		& a,
		& button {
			display: flex;
			align-items: center;
			justify-content: center;
			gap: 16px;

			height: 40px;
			padding: 0 16px;
			border-radius: 8px;
			width: 180px;

			color: var(--ft2);
			fill: currentColor;
			text-decoration: none;
			font-size: 0.8rem;

			& .name {
				display: flex;
				align-items: center;
				justify-content: space-between;
				width: 100%;
			}

			transition:
				background-color 0.2s ease-in-out,
				color 0.2s ease-in-out,
				font-weight 0.2s ease-in-out;

			&.active {
				anchor-name: --active;
				color: var(--ft1);
				background-color: var(--bg2);
				font-weight: 800;
			}

			&:hover {
				background-color: var(--bg1);
			}
		}
	}
</style>
