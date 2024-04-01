<script>
	import { state, user } from '$lib/store.js';
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Center from '$lib/center.svelte';
</script>

<Meta title="Admin Dashboard" description="This is an area for users with elevated permission." />

<Center>
	<br />
	<div class="ctitle">Dashboard</div>
</Center>

<Card>
	<div class="block">
		{#if $user.permissions.includes('user:view')}
			<Button class="wide" href="/admin/users">Users</Button>
			<br />
			<Button class="wide" href="/admin/admin_users">Admin Users</Button>
			<br />
		{/if}
		{#if $user.permissions.includes('voucher:view')}
			<Button class="wide" href="/admin/vouchers">Vouchers</Button>
			<br />
		{/if}
		{#if $user.permissions.includes('item:advert')}
			<Button class="wide" href="/admin/adverts">Adverts</Button>
			<br />
		{/if}
		{#if $user.permissions.includes('admin:manage_photo')}
			<Button class="wide" href="/admin/photo_error">Photo Error</Button>
			<br />
		{/if}

		<br /> TODO:
		<br />
		<br /> [ - ] fix page meta data / add to all pages
		<br /> [ - ] add sort and search to page with many entities
		<br /> [ - ] move view/get logs to frontend
		<br /> [ - ] more logs
		<br /> [ - ] fix cron
		<br />
		<br /> [ - ] move old_price to logs
		<br /> [ - ] does going back restore token
		<br /> [ - ] ADD "You may also like" user item group
		<br /> [ - ] use version for financial ops
		<br />
		<br /> [ - ] integrate AI assistant
		<br /> [ - ] update brand guide
		<br /> [ - ] write test
		<br /> [ - ] address api: www.geoapify.com/tutorials
	</div>
</Card>

<style>
	.block {
		max-width: 400px;
	}
</style>
