<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Tag from './search.tag.svelte';

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
		}
	});

	export let tags = [];
	export let page_name;
	let search = '';
</script>

<section>
	<Tag {tags} {page_name} />
	|
	<div class="input">
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

		<div class="search">
			<SVG type="search" size="15" />
		</div>

		{#if search}
			<div class="clear">
				<Button
					class="small round"
					on:click={() => {
						search = '';
						set_state(page_name, 'search', '');
					}}
				>
					<SVG type="close" size="15" />
				</Button>
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
		align-items: center;

		margin-top: var(--sp2);
		border: 2px solid var(--ac3);
		border-radius: var(--sp0) 0 0 var(--sp0);
	}

	.input {
		position: relative;
		width: 100%;
	}

	input {
		border: none;
		padding: 0 calc(var(--sp3) + var(--sp3));
	}

	.clear,
	.search {
		position: absolute;
		top: 0;
		height: 100%;

		display: flex;
		align-items: center;
	}
	.search {
		left: var(--sp2);
	}
	.clear {
		right: var(--sp2);
	}
</style>
