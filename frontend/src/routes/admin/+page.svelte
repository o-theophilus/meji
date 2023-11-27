<script>
	import { state, user } from '$lib/store.js';
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Center from '$lib/center.svelte';
</script>

<Meta title="Admin Dashboard" description="Admin Dashboard" />

<Center>
	<br />
	<div class="ctitle">Dashboard</div>
</Center>

<Card>
	<div class="block">
		{#if $user.roles.includes('user:view')}
			<Button class="wide" href="/admin/users">Users</Button>
			<br />
			<Button class="wide" href="/admin/admin_users">Admin Users</Button>
			<br />
		{/if}
		{#if $user.roles.includes('voucher:view')}
			<Button class="wide" href="/admin/vouchers">Vouchers</Button>
			<br />
		{/if}
		{#if $user.roles.includes('item:advert')}
			<Button class="wide" href="/admin/adverts">Adverts</Button>
			<br />
		{/if}
		{#if $user.roles.includes('admin:manage_photo')}
			<Button class="wide" href="/admin/photo_error">Photo Error</Button>
			<br />
		{/if}

		[ - ] cancel order email to admin and user
		<br />
		[ - ] terms and conditions
		<br />
		[ - ] does going back restore token
		<br />
		[ - ] address api: https://www.geoapify.com/tutorials
	</div>
</Card>

<style>
	.block {
		max-width: 400px;
	}
</style>
