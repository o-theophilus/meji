<script>
	import Card from '$lib/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/button.svelte';
</script>

<svelte:head>
	<title>Admin Dashboard | Meji</title>
</svelte:head>

<Card>
	<Title title="Dashboard" />
	<Body>
		<Button class="wide2" name="Order" href="/admin/order" />
		<Button class="wide2" name="Ad" href="/admin/ad" />
		<Button class="wide2" name="Voucher" href="/admin/voucher" />
		<Button class="wide2" name="tag" href="/admin/tag" />
		<Button class="wide2" name="User" href="/admin/user" />
	</Body>
</Card>
