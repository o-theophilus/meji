<script>
	import { createEventDispatcher } from 'svelte';

	const emit = createEventDispatcher();

	export let quantity = 1;

	const change = () => {
		emit('done', { quantity });
		if (quantity < 1) {
			quantity = 1;
		}
	};

	let clientWidth;
</script>

<!-- <button
	on:click={() => {
		qty = 0;
		change();
	}}
>
	x
</button> -->
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
		style:width="{clientWidth}px"
		bind:value={quantity}
		on:change={() => {
			change();
		}}
	/>
	<div class="helper" bind:clientWidth>
		{quantity}
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
		--size: 40px;

		display: flex;
		align-items: center;

		border: 2px solid var(--background);
		border-radius: var(--brad1);

		padding: 0 var(--gap1);
		width: min-content;
	}
	button,
	input {
		width: var(--size);
		height: var(--size);

		color: var(--font2);
		background: none;
		border: none;
	}
	.helper {
		position: absolute;
		visibility: hidden;

		padding: var(--gap1);
	}
	button {
		--size: 24px;

		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--gap2);

		width: var(--size);
		height: var(--size);

		border-radius: 50%;
	}
	input {
		padding: var(--gap1);
	}
	button:hover {
		background-color: var(--color1);
		color: var(--light_color);
	}

	input:hover {
		background-color: var(--background);
	}
	input:focus {
		background-color: var(--background);
	}
</style>
