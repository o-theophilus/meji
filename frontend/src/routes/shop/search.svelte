<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('tag')) {
			tag = params.get('tag');
		}
		if (params.has('search')) {
			search = params.get('search');
		}
	});

	export let tags = [];
	export let page_name = '';
	let tag = 'all';
	let search = '';
</script>

<section>
	<select
		bind:value={tag}
		on:change={() => {
			set_state(page_name, 'tag', tag != 'all' ? tag : '');
		}}
	>
		<option value="all" selected>all</option>
		{#each tags as x}
			<option value={x}>
				{x}
			</option>
		{/each}
	</select>

	<div class="search_area">
		<input
			type="text"
			placeholder="Search for product"
			bind:value={search}
			on:keypress={(e) => {
				if (e.key == 'Enter') {
					set_state(page_name, 'search', search);
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
						set_state(page_name, 'search', '');
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
			set_state(page_name, 'search', search);
		}}
	/>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp1);
		margin-top: var(--sp2);
	}

	select,
	option {
		text-transform: capitalize;
		width: unset;
	}

	.search_area {
		display: flex;
		gap: var(--sp1);

		position: relative;

		width: 100%;
	}

	select,
	input {
		border: 2px solid var(--ac3);
	}
	select:focus,
	input:focus {
		border-color: var(--cl1);
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
