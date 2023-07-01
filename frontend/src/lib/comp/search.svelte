<script>
	import { createEventDispatcher } from 'svelte';
	import { state, page_name } from '$lib/page_state.js';

	import Button from '$lib/comp/button.svelte';

	let emit = createEventDispatcher();

	let value = $state[$page_name].search;

	const submit = (v) => {
		value = v;
		$state[$page_name].search = v;
		emit('ok');
	};
</script>

<section>
	<div class="search_area">
		<input
			type="text"
			placeholder="Search for product"
			bind:value
			on:keypress={(e) => {
				if (e.key == 'Enter') {
					submit(value);
				}
			}}
		/>

		{#if value}
			<div
				class="clear"
				on:keypress
				on:click={() => {
					submit('');
				}}
			>
				✖
			</div>
		{/if}
	</div>

	<Button
		name="Search"
		icon="search"
		icon_size="15"
		class="tiny"
		on:click={() => {
			submit(value);
		}}
	/>
</section>

<style>
	section {
		/* margin-bottom: var(--gap1); */

		display: flex;
		gap: var(--gap1);
		padding: var(--gap1) var(--gap2);
		border-top: 2px solid var(--background);
	}

	.search_area {
		display: flex;
		gap: var(--gap1);

		position: relative;

		width: 100%;
	}

	input {
		width: 100%;
		height: var(--gap2);

		padding: var(--gap2);
		padding-right: 60px;

		border-radius: var(--brad1);
		border: 2px solid var(--background);

		color: var(--font1);
		background-color: var(--background);
	}
	input:hover {
		border-color: var(--midtone);
	}
	input:focus {
		border-color: var(--color1);
		background-color: var(--foreground);
	}

	.clear {
		--size: 20px;

		position: absolute;
		top: calc(50% - var(--size) / 2);
		right: calc(var(--size) / 2);

		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);

		border-radius: 50%;
		color: var(--font1);
		background: var(--background);
		cursor: pointer;
	}
	.clear:hover {
		background: var(--color4);
	}
</style>
