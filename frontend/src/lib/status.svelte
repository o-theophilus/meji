<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	export let page_name;
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

<div class="status">
	<div class="buttons">
		{#each array as x}
			<Button
				class={value == x ? 'primary' : ''}
				on:click={() => {
					if (x != value) {
						value = x;
						set_state(page_name, 'status', value == default_value ? '' : value);
					}
				}}
			>
				{x}
			</Button>
		{/each}
	</div>

	<div class="special">
		<slot />
	</div>
</div>

<style>
	.status {
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

	.special {
		padding-left: var(--sp1);
		border-left: 2px solid var(--ac4);
		flex-shrink: 0;
	}
</style>
