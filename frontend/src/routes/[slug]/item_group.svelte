<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { FoldButton } from '$lib/button';
	import { Spinner } from '$lib/macro';
	import One from './item_group.one.svelte';

	let { group, refresh, loading } = $props();
	let open = $derived(group.open);
</script>

{#if loading || group.items.length > 0}
	<div class="title line nowrap">
		<div class="line">
			{group.name}
			<Spinner active={loading} size="20" />
		</div>

		{#if !loading}
			<FoldButton
				{open}
				onclick={() => {
					open = !open;
				}}
			/>
		{/if}
	</div>

	{#if open && !loading}
		<div class="item_area" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each group.items as item, i}
				<One {item} {refresh} can_hide={i > 3}></One>
			{/each}
		</div>
	{/if}
{/if}

<style>
	.title {
		justify-content: space-between;
		margin-top: 40px;
		margin-bottom: 8px;
		font-weight: 800;
		color: var(--ft1);
	}

	.item_area {
		display: grid;
		grid-template-columns: 1fr 1fr;
		--gap: 8px;
		gap: var(--gap);

		@media screen and (min-width: 600px) {
			& {
				grid-template-columns: 1fr 1fr 1fr;
			}
		}
	}
</style>
