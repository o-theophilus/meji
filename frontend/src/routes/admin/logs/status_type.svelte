<script>
	import { set_state } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	export let page_name;
	export let actions;
	export let type;
	export let action;
</script>

<div class="block">
	<Button
		class="small {type == '' ? 'primary' : ''}"
		on:click={() => {
			type = '';
			action = '';
			set_state(page_name, 'status', '');
		}}
	>
		all
	</Button>
	{#each Object.keys(actions) as x}
		<Button
			class="small {x == type ? 'primary' : ''}"
			on:click={() => {
				type = x;
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

		align-items: center;
	}
</style>
