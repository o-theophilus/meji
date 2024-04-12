<script>
	import { createEventDispatcher } from 'svelte';

	const emit = createEventDispatcher();

	export let value = 1;
	export let min = 1;
	export let id = '';

	const change = () => {
		if (!Number.isInteger(value) || value < 0) {
			value = min;
		} else if (value < min) {
			value = min;
		}
		emit('change', value);
	};

	let clientWidth;
</script>

<section>
	<button
		on:click={() => {
			value -= 1;
			change();
		}}
	>
		-
	</button>

	<input
		type="number"
		{id}
		style:width="calc({clientWidth}px + 4px)"
		bind:value
		on:change={() => {
			change();
		}}
	/>

	<div class="helper" bind:clientWidth>
		{#if value}
			{value}
		{:else}
			0
		{/if}
	</div>

	<button
		on:click={() => {
			value += 1;
			change();
		}}
	>
		+
	</button>
</section>

<style>
	section {
		--size: var(--sp1);
		--height: 40px;

		display: flex;

		width: fit-content;
		border-radius: var(--sp0);
		overflow: hidden;

		color: var(--ac3);
		outline: 2px solid var(--ac4);
	}
	section:hover {
		outline-color: var(--ac3);
	}
	section:has(input:focus) {
		outline-color: var(--ac1);
	}

	input {
		padding: var(--size);
		height: var(--height);
		border: none;

		text-align: center;
		color: var(--ac1);
		background-color: var(--ac5);
	}

	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	.helper {
		position: absolute;
		padding: var(--sp1);
		visibility: hidden;

		min-width: var(--height);
	}

	button {
		aspect-ratio: 1/1;
		height: var(--height);

		background-color: var(--ac6);
		color: var(--ac2);
		border: none;
		cursor: pointer;
		font-weight: 700;
	}

	button:hover {
		background-color: var(--cl1_b);
		color: var(--ac6_);
	}
</style>
