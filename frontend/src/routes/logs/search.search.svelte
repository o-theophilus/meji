<script>
	import { createEventDispatcher } from 'svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	let emit = createEventDispatcher();

	export let placeholder = 'Search';
	export let search;
	export let show_search = false;
</script>

<div class="block" class:show_search>
	<div class="input">
		<div class="float svg">
			<SVG type="search" size="15" />
		</div>

		<input class:show_close={search != ''} type="text" {placeholder} bind:value={search} />

		<div class="float clear">
			{#if search}
				<Button
					class="small round"
					on:click={() => {
						search = '';
					}}
				>
					<SVG type="close" size="15" />
				</Button>
			{/if}
		</div>
	</div>

	<button
		class="primary"
		on:click={() => {
			emit('ok');
		}}
	>
		Search
	</button>
</div>

<style>
	.block {
		display: flex;
	}
	.input {
		position: relative;

		display: flex;
		align-items: center;

		width: 100%;

		fill: var(--ac3);
	}

	input {
		padding: var(--sp2);
		border: 2px solid var(--ac4);
		border-radius: var(--sp1);
		padding-left: var(--sp5);

		color: var(--ac1);
	}

	.show_search input {
		border-right: none;
		border-radius: var(--sp1) 0 0 var(--sp1);
	}

	input:hover,
	input:focus {
		border-color: var(--ac3);
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
		right: var(--sp2);
	}

	.svg {
		left: var(--sp2);
	}

	button {
		display: none;

		padding: var(--sp2) var(--sp3);
		border: none;
		border-radius: 0 var(--sp1) var(--sp1) 0;
		background-color: var(--cl1);
		color: var(--ac5_);
		cursor: pointer;
	}
	.show_search button {
		display: unset;
	}
	button:hover {
		background-color: var(--cl2);
	}
	button:disabled {
		background-color: var(--ac3);
		color: var(--ac4_);
		cursor: unset;
	}
</style>
