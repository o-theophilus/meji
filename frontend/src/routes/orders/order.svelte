<script>
	import { user } from '$lib/store.js';

	export let order;
	export let is_admin;
</script>

<a href="/orders/{order.key}">
	<div class="name">
		{#if order.user_key == $user.key && is_admin}
			*
		{/if}

		{order.key.substring(0, 8)}
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

		text-decoration: none;
		color: var(--ac2);
	}

	.name {
		font-weight: 700;
		color: var(--ac1);
	}
</style>
