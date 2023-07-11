<script>
	import Button from '$lib/button.svelte';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();

	let search;

	const submit = (v) => {
		emit('ok', { search });
	};
</script>

<section>
	<div class="search_area">
		<input
			type="text"
			placeholder="Search for product"
			bind:value={search}
			on:keypress={(e) => {
				if (e.key == 'Enter') {
					submit(search);
				}
			}}
		/>

		{#if search}
			<div class="clear">
				<Button
					icon="search"
					icon_size="15"
					class="tiny"
					on:click={() => {
						submit('');
					}}
				/>
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
			submit(search);
		}}
	/>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp1);
		margin-top: var(--sp2);
	}

	.search_area {
		display: flex;
		gap: var(--sp1);

		position: relative;

		width: 100%;
	}

	input {
		width: 100%;
		height: var(--sp2);

		padding: var(--sp2);
		padding-right: 60px;

		border-radius: var(--sp0);
		border: 2px solid transparent;

		color: var(--ac1);
		background-color: var(--ac3);
	}
	input:hover {
		border-color: var(--cl1);
	}
	input:focus {
		border-color: var(--cl1);
		background-color: var(--ac5);
	}

	.clear {
		--size: 20px;

		position: absolute;
		top: 7px;
		right: 10px;

		display: flex;
		justify-content: center;
		align-items: center;
	}
	.clear:hover {
		background-color: var(--cl4);
	}
</style>
