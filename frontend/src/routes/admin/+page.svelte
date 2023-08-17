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
	<Button class="wide2" name="Photos" href="/admin/photos" />
	<br />
	<Button class="wide2" name="Voucher" href="/admin/vouchers" />
	<br />
	<Button class="wide2" name="Ad" href="/admin/ad" />
	<br />
	<Button class="wide2" name="tag" href="/admin/tag" />
	<br />
	<Button class="wide2" name="User" href="/admin/user" />
</Card>
