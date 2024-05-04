<script>
	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';
	import Meta from '$lib/meta.svelte';
	import Back from '$lib/button/back.svelte';
	import Trx from './trx.svelte';

	export let data;
	export let { transactions } = data;
</script>

<Meta title="Transaction" description="Transaction" />

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			Transaction{transactions.length > 1 ? 's' : ''}
		</div>
	</div>
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
