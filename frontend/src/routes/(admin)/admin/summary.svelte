<script>
	import { Icon } from '$lib/macro';

	let { title, data, money, icon } = $props();
	let change = $derived(((data.value - data.prev_value) * 100) / data.value);
	let up = data.value > data.prev_value;
</script>

<div class="icon_tv">
	{#if icon}
		<div class="icon">
			<Icon {icon}></Icon>
		</div>
	{/if}

	<div class="tv">
		<div class="title">
			{title}
		</div>

		<div class="value">
			{#if money}
				₦{Number(data.value).toLocaleString()}
			{:else}
				{data.value}
			{/if}
		</div>
	</div>
</div>

<div class="change" class:down={!up}>
	{#if up}
		<Icon icon="trending-up"></Icon>
	{:else}
		<Icon icon="trending-down"></Icon>
	{/if}
	{change.toFixed(0)}%

	{#if up}
		increase
	{:else}
		decrease
	{/if}

	from yesterday
</div>

<style>
	.icon_tv {
		display: flex;
		gap: 8px;

		.icon {
			color: var(--ft1);
			display: flex;
			align-items: center;
			justify-content: center;

			background-color: var(--icon-color, var(--bg2));
			border-radius: 40%;

			width: 40px;
			height: 40px;
			flex-shrink: 0;
		}
	}

	.title {
		font-size: 0.8rem;
	}

	.value {
		font-weight: 800;
		font-size: 1.2rem;
		color: var(--ft1);
	}
	.change {
		font-size: 0.8rem;
		color: green;

		&.down {
			color: red;
		}
	}
</style>
