<script>
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button.svelte';

	const emit = createEventDispatcher();

	export let quantity = 1;
	export let min = 1;
	export let id = '';

	const change = () => {
		if (!Number.isInteger(quantity) || quantity < 0) {
			quantity = min;
		} else if (quantity < min) {
			quantity = min;
		}
		emit('done', { quantity });
	};

	let clientWidth;
</script>

<section>
	<Button
		on:click={() => {
			quantity -= 1;
			change();
		}}
	>
		-
	</Button>

	<input
		type="number"
		{id}
		style:width="calc({clientWidth}px + 4px)"
		bind:value={quantity}
		on:change={() => {
			change();
		}}
	/>
	<div class="helper" bind:clientWidth>
		{#if quantity}
			{quantity}
		{:else}
			0
		{/if}
	</div>

	<Button
		on:click={() => {
			quantity += 1;
			change();
		}}
	>
		+
	</Button>
</section>

<style>
	section {
		position: relative;

		display: flex;
		align-items: center;
		gap: 1px;
	}

	input {
		padding: var(--sp1);
		min-width: 40px;
		text-align: center;
	}
	input:focus {
		background-color: var(--ac6);
	}
	.helper {
		position: absolute;
		padding: var(--sp1);
		visibility: hidden;
	}
</style>
