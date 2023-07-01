<script>
	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';

	export let order;
	$: r = order.recipient;
	$: a = r.address;
	$: complete_address =
		r.name && r.phone && a.line && a.state && a.country && a.local_area && a.postal_code;
</script>

<Card>
	<Title title="Shipping Information">
		<slot {complete_address} />
	</Title>
	<Body>
		<span> Recipient: </span>
		Name:
		{#if r.name}
			{r.name}
		{:else}
			No Name
		{/if}
		<br />
		Phone:
		{#if r.phone}
			{r.phone}
		{:else}
			No Phone
		{/if}
		<br />
		<br />
		<span> Address: </span>
		{#if complete_address}
			{a.line}, {a.local_area} , {a.state} , {a.country} , {a.postal_code}
		{:else}
			No Address
		{/if}
	</Body>
</Card>

<style>
	span {
		font-weight: 500;
	}
</style>
