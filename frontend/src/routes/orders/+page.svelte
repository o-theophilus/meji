<script>
	import { user, set_state } from '$lib/store.js';
	import { page } from '$app/stores';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Status from '$lib/status.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Center from '$lib/center.svelte';

	export let data;
	$: orders = data.orders;
	$: total_page = data.total_page;
	let { page_name } = data;

	let status = ['pending', 'ordered', 'processing', 'enroute', 'delivered', 'canceled'];
</script>

<Meta title="Order" description="Order" />

<Center>
	<br />
	<b>
		{$page.url.searchParams.has('admin') ? 'All' : 'My'} Orders
	</b>
</Center>

<Card>
	<Status {page_name} {status} default_value="ordered">
		{#if $user.roles.includes('admin')}
			<Button
				class="small {$page.url.searchParams.has('admin') ? 'primary' : ''}"
				on:click={() => {
					if ($page.url.searchParams.has('admin')) {
						set_state(page_name, 'admin', '');
					} else {
						set_state(page_name, 'admin', 'true');
					}
				}}
			>
				{$page.url.searchParams.has('admin') ? 'All' : 'My'} Orders
			</Button>
		{/if}
	</Status>

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

	<Pagination {total_page} {page_name} />
</Card>

<style>
	b {
		color: var(--ac1);
	}

	.space:not(:last-child) {
		margin-top: var(--sp1);
	}
	.small {
		font-weight: normal;
		font-size: smaller;
	}
</style>
