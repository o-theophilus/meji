<script>
	import { page } from '$app/stores';
	import { user } from '$lib/store.js';

	export let order;
	console.log(order);
</script>

<a href="/orders/{order.key}">
	<div class="name">
		{#if order.user == $user.key && $page.url.searchParams.has('admin')}
			*
		{/if}

		{order.key}
	</div>

	{#each order.items as y, i}
		{#if i != 0},{/if}
		{y.name}
	{/each}
</a>

<style>
	a {
		display: block;
		padding: var(--sp2) 0;
		border-bottom: 1px solid var(--ac4);
		color: var(--ac2);

		text-decoration: none;
	}

	.name {
		font-weight: 500;
		color: var(--ac1);
	}
</style>
