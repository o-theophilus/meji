<script>
	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Status_Bar from './status.svelte';

	export let data;
	$: orders = data.orders;
	$: total_page = data.total_page;
</script>

<Meta title="Order" description="Order" />
<Status_Bar page_name="user_orders" />

<Card>
	<b> My Orders </b>
	<br />
	<br />
	{#each orders as x}
		<div>
			<Button class="wide" href="/orders/{x.key}">
				{x.key}
				<div class="fmt">
					{#each x.items as y, i}
						{#if i != 0},{/if}
						{y.name}
					{/each}
				</div>
			</Button>
		</div>
	{:else}
		no item here
	{/each}
</Card>

<style>
	.fmt {
		font-weight: normal;
		font-size: smaller;
	}
</style>
