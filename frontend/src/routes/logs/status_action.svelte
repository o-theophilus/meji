<script>
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';

	export let page_name;
	export let actions;
	export let type;
	export let status;
</script>

{#if type}
	<div class="buttons">
		{#each actions[type] as x}
			{@const action_ = `${type}:${x}`}
			<Button
				class="small {status == action_ ? 'primary' : ''}"
				on:click={() => {
					status = action_;
					set_state(page_name, 'status', action_);
				}}
			>
				{x}
			</Button>
		{/each}
	</div>
{/if}

<style>
	.buttons {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;

		margin-top: var(--sp2);

		align-items: center;
	}
</style>
