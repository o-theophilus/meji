<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Tag from './tag.svelte';

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
		}
	});

	export let tags = [];
	export let page_name = '';
	let search = '';
</script>

<section>
	<Tag {tags} {page_name} />

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
					class="small"
					on:click={() => {
						set_state(page_name, 'search', '');
					}}
				>
					<SVG type="search" size="15" />
				</Button>
				✖
			</div>
		{/if}
	</div>

	<Button
		class="primary"
		on:click={() => {
			set_state(page_name, 'search', search);
		}}
	>
		<SVG type="search" size="15" />
		Search
	</Button>
</section>

<style>
	section {
		display: flex;
		margin-top: var(--sp2);
	}

	.search_area {
		display: flex;
		gap: var(--sp1);

		position: relative;

		width: 100%;
	}

	input {
		border: 2px solid var(--ac3);
	}
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
