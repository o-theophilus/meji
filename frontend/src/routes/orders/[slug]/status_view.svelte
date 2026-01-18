<script>
	let { status, order_status } = $props();
</script>

<div class="status_block">
	{#if order_status == 'canceled'}
		<div class="status canceled">canceled</div>
	{:else if order_status == 'delivered'}
		<div class="status active">delivered</div>
	{:else}
		{#each status as x}
			{#if x != 'canceled'}
				<div class="status" class:active={x == order_status}>
					{x}
				</div>
			{/if}
		{/each}
	{/if}
</div>

<style>
	.status_block {
		display: flex;
		gap: 2px;

		margin-top: 4px;
		padding: 8px;
		border: 2px solid var(--bg3);
		border-radius: 8px;
	}

	.status {
		display: flex;
		justify-content: center;
		width: 100%;
		padding: 4px 0;
		border-radius: 4px;

		color: white;
		font-size: 0.8rem;
		background-color: rgb(0, 65, 0);
		text-transform: capitalize;
	}

	.active {
		background-color: green;
		color: white;
	}
	.active ~ .status {
		color: var(--ft2);
		background-color: var(--bg3);
	}

	.canceled {
		background-color: red;
		color: white;
	}
</style>
