<script>
	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';
	import Meta from '$lib/meta.svelte';

	// export let data;
	// let { activities } = data;
	export let transactions = [];
</script>

<Meta title="Transaction" description="Transaction" />

<Center>
	<br />
	<div class="ctitle">
		Transaction{transactions.length > 1 ? 's' : ''}
	</div>
</Center>

<Card>
	{#each transactions as trans}
		{trans.key} - {trans.value}
		<br />
	{:else}
		no item here
	{/each}
</Card>

<style>
</style>
