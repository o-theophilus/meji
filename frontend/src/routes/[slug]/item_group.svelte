<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { FoldButton } from '$lib/button';
	import { Spinner } from '$lib/macro';
	import One from "./item_group.one.svelte"

	let { group, refresh, loading } = $props();
	let open = $derived(group.open);
</script>

{#if loading || group.items.length > 0}
	<div class="title line">
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
	<div class="item_area">

		<div class="scroller" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			
			{#each group.items as item}
			<One {item} {refresh}></One>
			{/each}
			
		</div>
		<!-- <button class=left>
			left
		</button>

		<button class=right>
			right
		</button> -->
	</div>
	{/if}
{/if}

<style>
	.title {
		justify-content: space-between;
		margin: 48px 0;
	}

	.item_area{
		position: relative;
	}
	
	.scroller {

		display: flex;
		--gap: 24px;
		gap: var(--gap);
		/* margin: 48px 0; */
		overflow-x: auto;
		scroll-snap-type: x mandatory;

		@media screen and (min-width: 600px) {
			& {
				grid-template-columns: 1fr 1fr;
			}
		}
	}

	button{
		all:unset;
		cursor: pointer;
		
	 	position: absolute;
		top: 10px;
		
		display: flex;
		align-items: center;
		justify-content: center;

		background-color: red;
		width: 40px;
		aspect-ratio: 1;
		border-radius: 50%;

		&.left{
			left: 0;
		}
		&.right{
			right: 0;
		}
	}

</style>
