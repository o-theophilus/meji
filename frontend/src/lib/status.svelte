<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Tag from '$lib/button/tag.svelte';

	export let array;
	export let default_value = '';
	let value = default_value;

	let set = (url) => {
		value = default_value;
		if (url.searchParams.has('status')) {
			value = url.searchParams.get('status');
		}
	};

	onMount(() => {
		set($page.url);
	});
	$: set($page.url);
</script>

<div class="component">
	<div class="buttons">
		{#each array as x}
			<Tag
				active={value == x}
				no_grow
				on:click={() => {
					if (x != value) {
						value = x;
						set_state('status', value == default_value ? '' : value);
					}
				}}
			>
				{x}
			</Tag>
		{/each}
	</div>

	<div class="right">
		<slot />
	</div>
</div>

<style>
	.component {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		justify-content: space-between;
	}

	.buttons {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;
	}

	.right {
		padding-left: var(--sp1);
		border-left: 2px solid var(--ac4);
		flex-shrink: 0;
	}
</style>
