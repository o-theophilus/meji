<script>
	import { state } from '$lib/store.js';
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
</script>

<Meta title="Admin Dashboard" description="Admin Dashboard" />

<Card>
	<b> Dashboard </b>
	<br />
	<br />
	<Button class="wide" href="/admin/users">Users</Button>
	<br />
	<Button class="wide" href="/admin/vouchers">Vouchers</Button>
	<br />
	<Button class="wide" href="/logs{$state.logs || '?admin=true'}">Logs</Button>
	<br />
	<Button class="wide" href="/admin/adverts">Adverts</Button>
	<br />
	<Button class="wide" href="/admin/photos">Photos</Button>
</Card>
