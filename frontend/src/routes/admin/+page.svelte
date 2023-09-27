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
	<Button class="wide" href="/admin/photo">Photo</Button>
	<br />
	<Button class="wide" href="/admin/voucher">Voucher</Button>
	<br />
	<Button class="wide" href="/admin/advert">Advert</Button>
	<br />
	<Button class="wide" href="/admin/log{$state.logs || ''}">Log</Button>
	<br />
	<Button class="wide" href="/admin/tag">tag</Button>
	<br />
	<Button class="wide" href="/admin/user">User</Button>
</Card>
