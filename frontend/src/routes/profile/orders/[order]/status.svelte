<script>
	import Card from '$lib/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';

	export let order;
</script>

<Card>
	<Title title="Order status" />
	<Body>{order.status}</Body>
</Card>

<style>
</style>
