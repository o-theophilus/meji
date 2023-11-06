<script>
	export let order;
	$: r = order.receiver;
	$: a = r.address;
</script>

<div class="bold">
	Receiver's Information:

	<slot />
</div>

<div class="grid">
	<div>Name:</div>
	<div>
		{#if r.name}
			{r.name}
		{:else}
			No Name
		{/if}
	</div>

	<div>Phone:</div>
	<div>
		{#if r.phone}
			{r.phone}
		{:else}
			No Phone
		{/if}
	</div>

	<div>Address:</div>
	<div>
		{#if a.line && a.state && a.country && a.local_area && a.postal_code}
			{a.line}, {a.local_area}, {a.state}, {a.country}, {a.postal_code}.
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
