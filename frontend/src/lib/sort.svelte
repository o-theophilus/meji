<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let page_name;
	export let array;
	export let default_value = '';
	let width;
	let open = false;

	const sort_items = (x) => {
		default_value = x;
		open = false;
		set_state(page_name, 'sort', x == 'latest' ? '' : x);
	};

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('sort')) {
			default_value = params.get('sort');
		}
	});
</script>

<svelte:window
	on:click={() => {
		if (open) {
			open = false;
		}
	}}
/>

<div bind:clientWidth={width} class="pos" on:click|stopPropagation role="presentation">
	<Button
		class="small"
		on:click={() => {
			open = !open;
		}}
	>
		<SVG type="list" />
		sort: {default_value}
	</Button>

	{#if open}
		<div class="sort" style:width="{width}px">
			{#each array as x}
				<button
					on:click={() => {
						sort_items(x);
					}}
				>
					{x}

					{#if x == default_value}
						<span> ✓ </span>
					{/if}
				</button>
			{/each}
		</div>
	{/if}
</div>

<style>
	.pos {
		position: inherit;
		z-index: 1;
	}

	.sort {
		display: flex;
		flex-direction: column;

		position: absolute;

		background-color: var(--ac5);
		border-radius: var(--sp0);
		border: 2px solid var(--ac3);
	}
	button {
		display: flex;
		justify-content: space-between;

		padding: var(--sp0) var(--sp1);
		border: none;
		background: none;
		color: var(--ac2);
	}

	button:hover {
		background-color: var(--cl1);
		color: var(--ac5_);
	}
</style>
