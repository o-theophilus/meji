<script>
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
</script>

<Meta title="Admin Dashboard" description="Admin Dashboard" />

<Card>
	<b> Dashboard </b>
	<br />
	<br />
	<Button class="wide" href="/admin/photos">Photos</Button>
	<br />
	<Button class="wide" href="/admin/vouchers">Voucher</Button>
	<br />
	<Button class="wide" href="/admin/ad">Ad</Button>
	<br />
	<Button class="wide" href="/admin/tag">tag</Button>
	<br />
	<Button class="wide" href="/admin/user">User</Button>
</Card>
