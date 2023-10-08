<script>
	import { state } from '$lib/store.js';
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
	<Button class="wide" href="/admin/users">Users</Button>
	<br />
	<Button class="wide" href="/admin/vouchers">Vouchers</Button>
	<br />
	<Button class="wide" href="/logs{$state.logs || ''}">Logs</Button>
	<br />
	<Button class="wide" href="/admin/adverts">Adverts</Button>
	<br />
	<Button class="wide" href="/admin/photos">Photos</Button>
	<br />
	make users admin
	<br />
	advert placement
	<br />
	cleanup unused photos
	<br />
	app setting
</Card>

<style>
</style>
