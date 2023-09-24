<script>
	import { user } from '$lib/store.js';
	import { page } from '$app/stores';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Status_Bar from './status.svelte';

	export let data;
	$: orders = data.orders;
	$: total_page = data.total_page;
</script>

<Meta title="Order" description="Order" />
<Status_Bar page_name="orders" />

<Card>
	<b> My Orders </b>
	<br />
	<br />
	{#each orders as x}
		<Button class="wide" href="/orders/{x.key}">
			<span>
				{#if x.user == $user.key && $page.url.searchParams.has('admin')}
					*
				{/if}
				{x.key}
				<span class="small">
					-
					{#each x.items as y, i}
						{#if i != 0},{/if}
						{y.name}
					{/each}
				</span>
			</span>
		</Button>
		<div class="space" />
	{:else}
		no item here
	{/each}
</Card>

<style>
	.space:not(:last-child) {
		margin-top: var(--sp1);
	}
	.small {
		font-weight: normal;
		font-size: smaller;
	}
</style>
