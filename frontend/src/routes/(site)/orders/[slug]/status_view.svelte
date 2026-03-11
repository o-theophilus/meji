<script>
	import { Datetime } from '$lib/macro';
	let { status, order } = $props();
</script>

<div class="status_block">
	{#if order.status == 'canceled'}
		<div class="status canceled">canceled</div>
	{:else if order.status == 'delivered'}
		<div class="status active">delivered</div>
	{:else}
		{#each status as x}
			{#if x != 'canceled'}
				<div class="status" class:active={x == order.status}>
					<div class="name">
						{x}
					</div>
					<div class="date">
						<Datetime datetime={order.timeline[x]} type="date_numeric" />
						<Datetime datetime={order.timeline[x]} type="time_12h" />
					</div>
				</div>
			{/if}
		{/each}
	{/if}
</div>

<style>
	.status_block {
		display: flex;
		flex-direction: column;
		gap: 2px;

		margin-top: 4px;
		padding: 4px;
		border: 1px solid var(--bg2);
		border-radius: 8px;
	}
	@media screen and (min-width: 400px) {
		.status_block {
			flex-direction: unset;
		}
	}

	.status {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		width: 100%;
		padding: 4px;
		border-radius: 4px;

		color: white;
		font-size: 0.8rem;
		text-align: center;
		background-color: rgb(0, 65, 0);
		text-transform: capitalize;
	}
	.name {
		font-weight: 800;
	}
	.date {
		font-size: 0.7rem;
		line-height: 120%;
	}

	.active {
		background-color: green;
		color: white;
	}
	.active ~ .status {
		color: var(--ft2);
		background-color: var(--bg2);
	}

	.canceled {
		background-color: red;
		color: white;
	}
</style>
