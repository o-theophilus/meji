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

		if (params.has('tag')) {
			let x = params.get('tag').split('$:');
			selected = x[0].split(',');
			logic = x[1];
		}
	});

	export let tags = [];
	export let page_name;

	let search = '';
	let show_tags = false;

	let selected = [];
	let selected_snap = [];
	let logic = 'or';
	let logic_snap = 'or';
</script>

<section>
	<button
		on:click={() => {
			show_tags = !show_tags;
			selected_snap = [...selected].sort((a, b) => a - b).join(',');
			logic_snap = `${logic}`;
		}}
	>
		Tags
	</button>

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

		{#if search}
			<div class="btn">
				<Button
					class="small round"
					on:click={() => {
						search = '';
						set_state(page_name, 'search', '');
					}}
				>
					<SVG type="close" size="15" />
				</Button>

				<Button
					class="round small"
					on:click={() => {
						set_state(page_name, 'search', search);
					}}
				>
					<SVG type="search" size="15" />
				</Button>
			</div>
		{/if}
	</div>

	{#if show_tags}
		<Tag
			{tags}
			{page_name}
			bind:selected
			bind:logic
			on:click={() => {
				show_tags = false;

				selected.sort((a, b) => a - b).join(',');
				if (selected != selected_snap || logic != logic_snap) {
					set_state(page_name, 'tag', `${selected}$:${logic}`);
				}
			}}
			role="presentation"
		/>
	{/if}
</section>

<style>
	section {
		position: relative;

		display: flex;
		align-items: center;

		margin-top: var(--sp2);
		border: 2px solid var(--ac3);
		border-radius: var(--sp0) 0 0 var(--sp0);
		color: var(--ac3);
	}
	button {
		padding: var(--sp2) var(--sp4);
		background: none;
		border: none;
		color: var(--ac1);
	}
	button:hover {
		background-color: var(--cl1);
	}
	.input {
		position: relative;
		width: 100%;
	}

	input {
		border: none;
		padding: 0 calc(var(--sp3) + var(--sp3));
	}

	.btn {
		position: absolute;
		top: 0;
		right: var(--sp2);

		display: flex;
		align-items: center;
		gap: var(--sp1);

		height: 100%;
	}
</style>
