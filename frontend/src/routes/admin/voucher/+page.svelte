<script>
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Status_Bar from './status.svelte';

	import { portal } from '$lib/store.js';

	export let data;
	$: vouchers = data.vouchers;
	$: total_page = data.total_page;

	$: if ($portal && $portal.type == 'voucher') {
		vouchers = $portal.data;
		$portal = '';
	}
</script>

<Meta title="Vouchers" description="Vouchers" />
<Status_Bar page_name="voucher" />

<Card>
	<b> Voucher{vouchers.length > 1 ? 's' : ''} </b>
	<br />
	<br />
	{#each vouchers as x}
		{x.date}
		<br />
		{x.status}
		<br />
		<a href="/admin/vouchers/{x.key}">
			{x.key}
		</a>
		<br />
		{x.value}
		<br />

		<br />
	{:else}
		no item here
	{/each}
</Card>

<style>
</style>
