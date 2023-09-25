<script>
	import { set_state } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	export let page_name = '';
	export let type = '';
	export let actions = [];
	export let status = '';
</script>

<div class="block">
	{#each actions as x}
		{@const x_ = `${type}:${x}`}
		<Button
			class="small {x_ == status ? 'primary' : ''}"
			on:click={() => {
				status = x_;
				set_state(page_name, 'status', x != 'all' ? x_ : '');
			}}
		>
			{x}
		</Button>
	{/each}
</div>

<style>
	.block {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;

		margin-top: var(--sp2);
	}
</style>
