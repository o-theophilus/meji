<script>
	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';
	import Meta from '$lib/meta.svelte';
	import Back from '$lib/button/back.svelte';
	import Trx from './trx.svelte';
	import Title from '$lib/title.svelte';

	export let data;
	export let { transactions } = data;
</script>

<Meta title="Transactions"  />

<Center>
	<Title card>
		<svelte:fragment slot="left">
			<Back />
		</svelte:fragment>
		Transaction{transactions.length > 1 ? 's' : ''}
	</Title>
</Center>

<Card>
	{#each transactions as trx}
		<Trx {trx} />
	{:else}
		no item here
	{/each}
</Card>

<style>
</style>
