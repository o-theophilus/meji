<script>
	import { Icon } from '$lib/macro';
	let { value = 0, size = 16, mini = false } = $props();

	let roundedValue = Math.round(value * 2) / 2;
</script>

<div class="rating">
	{#if mini}
		<div class="mini">
			{Number(value).toFixed(1)}
			<Icon icon="star" {size} />
		</div>
	{:else}
		<div class="full">
			{#each Array(5) as _, i}
				<div class="one">
					<div class="half" class:active={roundedValue > i}>
						<Icon icon="star-half" {size}></Icon>
					</div>
					<div class="half right" class:active={roundedValue > i + 0.5}>
						<Icon icon="star-half" {size}></Icon>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.rating {
		width: fit-content;
		padding: var(--ratig-padding, 0);
		border-radius: 4px;
		background-color: var(--rating-background-color, transparent);
	}

	.full {
		display: flex;
		--icon-stroke-width: 1;
		--icon-fill: var(--ft2);
		--icon-stroke: var(--ft2);
	}

	.one {
		position: relative;
	}
	.half {
		line-height: 80%;
	}

	.right {
		position: absolute;
		top: 0;
		left: 0;
		transform: scaleX(-1);
	}

	.full .active {
		--icon-fill: goldenrod;
		--icon-stroke: goldenrod;
	}

	.mini {
		display: flex;
		align-items: center;
		gap: 2px;

		line-height: 100%;
		color: hsl(0, 0%, 80%);
		font-size: 0.8rem;

		--icon-fill: goldenrod;
		--icon-stroke: goldenrod;
		--icon-stroke-width: 1;
	}
</style>
