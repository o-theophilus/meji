<script>
	import { Icon } from '$lib/macro';
	// import Bar from './rating.bar.svelte';

	let { ratings } = $props();
	let info = $derived.by(() => {
		let _count = 0;
		let _sum = 0;
		for (const x of ratings) {
			_count += x.count;
			_sum += x.rating * x.count;
		}
		let avg = _sum / _count;

		return { count: _count, sum: _sum, average: avg.toFixed(1) };
	});
</script>

{#if info.count}
	<section>
		<div class="left">
			<span class="small"> <span class="average">{info.average}</span>/5 </span>
			<Icon icon="star" size="30" />
			<span class="small">
				{info.count} review{#if info.count > 1}s{/if}
			</span>
		</div>

		<div class="right">
			{#each ratings as rating}
				<div class="info small">
					{rating.rating}
					<Icon icon="star" size="12" />
					{rating.count}
					<div class="user">
						<Icon icon="user" size="10" />
					</div>
				</div>
				<div class="bar">
					<div class="fill" style:width="{(rating.count * 100) / info.count}%"></div>
				</div>
			{/each}
		</div>
	</section>
{/if}

<style>
	.small {
		font-size: 0.8rem;
	}
	section {
		display: flex;
		align-items: center;
		gap: 24px;

		--icon-stroke-width: 1;
		--icon-fill: goldenrod;
		--icon-stroke: goldenrod;
	}

	.left {
		display: flex;
		align-items: center;
		flex-direction: column;

		padding: 16px;
		flex-shrink: 0;
	}

	.average {
		font-size: 1.2rem;
		font-weight: 800;
	}

	.right {
		width: 100%;
		display: grid;
		grid-template-columns: max-content auto;
		align-items: center;
		gap: 0 16px;
	}

	.info {
		display: flex;
		align-items: center;
		gap: 4px;
	}

	.user {
		fill: var(--ft2);
	}

	.bar {
		width: 100%;
		height: 10px;
		background-color: var(--bg2);
		border-radius: 5px;
		outline: 1px solid var(--bg);
		outline-offset: -1px;
	}

	.fill {
		height: 100%;
		background-color: goldenrod;
		border-radius: 5px;
		transition: width 1s ease-in-out;
	}
</style>
