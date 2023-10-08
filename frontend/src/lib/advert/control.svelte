<script>
	import { createEventDispatcher } from 'svelte';
	let emit = createEventDispatcher();

	export let count;
	export let index = 0;
</script>

{#if count > 1}
	<div class="control">
		{#each Array(count) as _, i}
			<div
				class="btn"
				class:active={index == i}
				on:keypress
				role="button"
				tabindex="0"
				on:click={() => {
					index = i;
					emit('ok', i);
				}}
			/>
		{/each}
	</div>
{/if}

<style>
	.control {
		position: absolute;
		bottom: 24px;

		display: flex;
		gap: var(--sp1);
		justify-content: center;

		width: 100%;
	}

	.btn {
		--size: 20px;

		width: var(--size);
		height: var(--size);

		border-radius: var(--size);

		background-color: var(--cl1);

		transition: var(--trans1);
	}

	.btn:hover {
		width: calc(var(--size) * 2.5);
	}

	.btn.active {
		width: calc(var(--size) * 2.5);
	}
</style>
