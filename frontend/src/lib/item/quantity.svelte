<script>
	import { createEventDispatcher } from 'svelte';

	import Button from '$lib/button.svelte';

	const emit = createEventDispatcher();

	export let quantity = 1;
	let def = quantity;

	const change = () => {
		if (!Number.isInteger(quantity) || quantity < 0) {
			quantity = def;
		} else if (quantity < 1) {
			quantity = 1;
			emit('done', { quantity: 0 });
		} else {
			def = quantity;
			emit('done', { quantity });
		}
	};

	let clientWidth;
</script>

<section>
	<Button
	
		on:click={() => {
			quantity -= 1;
			change();
		}}>-</Button
	>

	<input
		type="number"
		style:width="calc({clientWidth}px + 4px)"
		min="0"
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
		}}>+</Button
	>
</section>

<style>
	section {
		position: relative;
		
		display: flex;
		align-items: center;
		gap: var(--sp0);
	}

	input {
		padding: var(--sp1);
		min-width: 40px;
		text-align: center;
	}
	input:focus {
		background-color: var(--ac5);
	}
	.helper {
		position: absolute;
		padding: var(--sp1);
		visibility: hidden;
	}
</style>
