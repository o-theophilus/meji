<script>
	import Nav from './admin_nav.svelte';

	let { children } = $props();
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
			icon: 'bar-chart-3'
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
			onclick: () => (open = !open),
			access: null,
			icon: 'clipboard-list'
		}
	];

	let ops = $state({ open: true });
</script>

<div class="container">
	<Nav bind:ops></Nav>

	<div class="page">
		{@render children()}
	</div>
</div>

<style>
	.container {
		display: flex;
		/* align-items: flex-end; */
		background-color: var(--bg1);
	}

	.page {
		width: 100%;
	}
</style>
