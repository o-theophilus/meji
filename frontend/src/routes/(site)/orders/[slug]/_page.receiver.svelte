<script>
	import { Icon } from '$lib/macro';
	let { receiver, top_right } = $props();
</script>

<div class="name">
	{receiver.name}

	{@render top_right?.()}
</div>

<div class="grid">
	<Icon icon="phone" size="12"></Icon>
	{receiver.phone}
	<Icon icon="mail" size="12"></Icon>
	{receiver.email}
	<Icon icon="map-pin" size="12"></Icon>
	{receiver.address.address}, {receiver.address.state}, {receiver.address.country}
	{#if receiver.address.postal_code}
		<Icon icon="hash" size="12"></Icon>
		{receiver.address.postal_code}
	{/if}
</div>

<style>
	.name {
		display: flex;
		justify-content: space-between;
		flex-wrap: wrap;
		color: var(--ft1);
	}

	.grid {
		display: grid;
		grid-template-columns: min-content auto;
		align-items: center;
		gap: 2px 8px;

		font-size: 0.8rem;
	}
</style>
