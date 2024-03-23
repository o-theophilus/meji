<script>
	export let order;
</script>

<div class="bold">
	Receiver's Information:

	<slot />
</div>

<div class="grid">
	<div>Name:</div>
	<div>
		{#if order.name}
			{order.name}
		{:else}
			No Name
		{/if}
	</div>

	<div>Phone:</div>
	<div>
		{#if order.phone}
			{order.phone}
		{:else}
			No Phone
		{/if}
	</div>

	<div>Address:</div>
	<div>
		{#if order.line && order.state && order.country && order.local_area && order.postal_code}
			{order.line}, {order.local_area}, {order.state}, {order.country}, {order.postal_code}.
		{:else}
			No Address
		{/if}
	</div>
</div>

<style>
	.bold {
		font-weight: 500;
		color: var(--ac1);
	}

	.grid {
		display: grid;
		gap: 0 var(--sp3);
		grid-template-columns: max-content auto;
	}
</style>
