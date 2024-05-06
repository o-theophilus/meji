<script>
	import { user } from '$lib/store.js';

	import Value from '$lib/item/variation_value.svelte';

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

	<span class="variation">
		{#each order.items as y, i}
			[
			<span class="name">{y.name}</span>{#each Object.entries(y.variation) as [key, value]}, {key}:
				<Value {value} />{/each}, quantity: <Value value={`${y.quantity}`} />]
		{/each}
	</span>
</a>

<style>
	a {
		display: block;

		padding-top: var(--sp2);
		margin-top: var(--sp2);
		border-top: 1px solid var(--ac4);

		text-decoration: none;
		color: var(--ac2);
	}

	.name {
		font-weight: 700;
		color: var(--ac1);
	}
</style>
