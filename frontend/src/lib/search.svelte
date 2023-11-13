<script>
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();

	export let placeholder = 'Search';
	export let search;
</script>

<div class="input">
	<div class="float svg">
		<SVG type="search" size="15" />
	</div>

	<input
		class:show_close={search != ''}
		type="text"
		{placeholder}
		bind:value={search}
		on:keypress={(e) => {
			if (e.key == 'Enter') {
				emit('ok');
			}
		}}
	/>

	<div class="float clear">
		{#if search}
			<Button
				class="round"
				on:click={() => {
					emit('clear');
				}}
			>
				<SVG type="close" size="8" />
			</Button>
		{/if}
	</div>
</div>

<style>
	.input {
		position: relative;

		display: flex;
		align-items: center;

		width: 100%;

		fill: var(--ac3);
	}

	input {
		width: 100%;
		padding: var(--sp1);
		border-radius: var(--sp0);
		padding-left: var(--sp5);
		border: none;

		outline: 2px solid var(--ac4);
		background-color: var(--ac5);
		color: var(--ac1);
	}

	input:hover {
		outline-color: var(--ac3);
	}

	input:focus {
		outline-color: var(--ac1);
	}

	.show_close {
		padding-right: var(--sp5);
	}

	.float {
		position: absolute;
		top: 0;
		display: flex;
		align-items: center;
		height: 100%;
	}

	.clear {
		right: var(--sp1);
	}

	.svg {
		left: var(--sp2);
	}
</style>
