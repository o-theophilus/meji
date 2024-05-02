<script>
	import { createEventDispatcher } from 'svelte';
	let emit = createEventDispatcher();

	export let count;
	let index = 0;

	const auto_scroll = () => {
		index += 1;
		if (index > count - 1) {
			index = 0;
		}
		emit('ok', index);
	};

	let timer = setInterval(auto_scroll, 1000 * 5);
	const reset_timer = () => {
		clearInterval(timer);
		timer = setInterval(auto_scroll, 1000 * 5);
	};
</script>

{#if count > 1}
	<div class="control">
		{#each Array(count) as _, i}
			<button
				class:active={index == i}
				on:click={() => {
					reset_timer();
					index = i;
					emit('ok', i);
				}}
			/>
		{/each}
	</div>
{/if}

<style>
	.control {
		padding: 24px;

		display: flex;
		gap: var(--sp1);

		width: fit-content;
	}

	button {
		--size: 20px;

		width: var(--size);
		height: var(--size);

		border: none;
		border-radius: var(--size);
		background-color: var(--ac6);
		transition: var(--trans1);

		cursor: pointer;
	}

	button:hover {
		background-color: var(--cl1);
	}

	button.active {
		width: calc(var(--size) * 2.5);
	}
</style>
