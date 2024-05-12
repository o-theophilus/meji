<script>
	import { user } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button/button.svelte';
	import Center from '$lib/center.svelte';
	import Title from '$lib/title.svelte';
</script>

<Meta title="Admin Dashboard" description="This is an area for users with elevated permission." />

<Center>
	<Title>Dashboard</Title>
</Center>

<Card>
	<div class="block">
		{#if $user.permissions.includes('user:set_permission')}
			<Button size="wide" href="/admin/admin_users">Admin Users</Button>
			<br />
		{/if}
		{#if $user.permissions.includes('user:view')}
			<Button size="wide" href="/admin/users">Users</Button>
			<br />
		{/if}
		{#if $user.permissions.includes('voucher:view')}
			<Button size="wide" href="/admin/vouchers">Vouchers</Button>
			<br />
		{/if}
		{#if $user.permissions.includes('item:advert')}
			<Button size="wide" href="/admin/adverts">Adverts</Button>
			<br />
		{/if}
		{#if $user.permissions.includes('admin:manage_photo')}
			<Button size="wide" href="/admin/photo_error">Photo Error</Button>
			<br />
		{/if}

		<br /> TODO:
		<br />
		<br /> [ - ] better page meta descriptions
		<br />
		<br /> [ - ] meji contacts
		<br /> [ - ] how changing item status and price of items affect save, advert and cart
		<br /> [ - ] how deleted users signup again
		<br /> [ - ] use version for financial ops
		<br /> [ - ] does going back restore token
		<br />
		<br /> [ - ] integrate AI assistant
		<br /> [ - ] use svelte runes
		<br /> [ - ] address api: www.geoapify.com/tutorials
		<br /> [ - ] update brand guide
		<br /> [ - ] write test
	</div>
</Card>

<style>
	.block {
		max-width: 400px;
	}
</style>
