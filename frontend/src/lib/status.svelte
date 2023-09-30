<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	export let page_name = '';
	export let status;
	export let default_value = '';
	let key = 'status';
	let value = default_value;

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has(key)) {
			value = params.get(key);
		}
	});
</script>

<div class="status">
	<div class="buttons">
		{#each status as x}
			<Button
				class="small {value == x ? 'primary' : ''}"
				on:click={() => {
					value = x;
					let v = x == default_value ? '' : x;
					set_state(page_name, key, v);
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
