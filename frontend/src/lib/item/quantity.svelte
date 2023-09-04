<script>
	import { createEventDispatcher } from 'svelte';

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
	<button
		on:click={() => {
			quantity -= 1;
			change();
		}}
	>
		-
	</button>

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
	<button
		on:click={() => {
			quantity += 1;
			change();
		}}
	>
		+
	</button>
</section>

<style>
	section {
		position: relative;
		gap: var(--sp0);

		display: flex;
		align-items: center;
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

	button {
		display: flex;
		justify-content: center;
		align-items: center;

		--size: 24px;
		width: var(--size);
		height: var(--size);

		border: none;
		color: var(--ac2);
		background-color: var(--ac4);
		border-radius: 50%;

		cursor: pointer;
	}

	button:hover {
		background-color: var(--cl1);
		color: var(--ac5_);
	}
</style>
