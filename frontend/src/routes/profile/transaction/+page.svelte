<script>
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';

	// export let data;
	// let { activities } = data;
	export let transactions = [];
</script>

<Meta title="Transaction" description="Transaction" />

<Card>
	<b> Transaction{transactions.length > 1 ? 's' : ''} </b>
	<br />
	<br />
	{#each transactions as trans}
		{trans.key} - {trans.value}
		<br />
	{:else}
		no item here
	{/each}
</Card>

<style>
</style>
