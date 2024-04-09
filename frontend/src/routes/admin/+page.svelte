<script>
	import { user } from '$lib/store.js';

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
		<br /> [ - ] better page meta descriptions
		<br />
		<br /> [ - ] use svelte runes
		<br /> [ - ] how changing status and price of items affect save, advert and cart
		<br /> [ - ] make order and voucher date time uniform
		<br />
		<br /> [ - ] fix cron
		<br /> [ - ] use version for financial ops
		<br /> [ - ] does going back restore token
		<br /> [ - ] update brand guide
		<br /> [ - ] integrate AI assistant
		<br /> [ - ] write test
		<br /> [ - ] address api: www.geoapify.com/tutorials
	</div>
</Card>

<style>
	.block {
		max-width: 400px;
	}
</style>
