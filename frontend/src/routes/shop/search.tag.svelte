<script>
	import { page } from '$app/stores';
	import { createEventDispatcher, onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	let emit = createEventDispatcher();

	export let tags;
	export let page_name;
	let selected = [];
	let logic = false;
	let search = '';
	let selected_snap = [];
	let logic_snap;

	$: old = selected_snap.sort((a, b) => a - b).join(',');
	$: sele = selected.sort((a, b) => a - b).join(',');
	$: changed = old != sele || (logic != logic_snap && selected.length > 1);

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('tag')) {
			let x = params.get('tag').split('$:');
			selected = x[0].split(',');
			logic = x[1] == 'true';
		}

		selected_snap = [...selected];
		logic_snap = logic;
	});
</script>

<svelte:window
	on:click={() => {
		emit('close');
	}}
/>

<section on:click|stopPropagation role="presentation">
	All Tags

	<br />
	<br />

	<div class="input">
		<input bind:value={search} type="text" placeholder="Search" />
		{#if search}
			<div class="clear">
				<Button
					class="round small"
					on:click={() => {
						search = '';
					}}
				>
					<SVG type="close" />
				</Button>
			</div>
		{/if}
	</div>

	<br />

	<div class="tags">
		{#each tags as x}
			<label class:hide={!x.includes(search)}>
				<input bind:group={selected} type="checkbox" value={x} />
				{x}
			</label>
		{/each}
	</div>

	<br />

	<div class="line">
		<label>
			<input bind:checked={logic} type="checkbox" />
			&&
		</label>

		<div class="line">
			<Button
				disabled={selected.length == 0}
				class="small hover_red"
				on:click={() => {
					selected = [];
					logic = false;
				}}
			>
				<SVG type="close" />
			</Button>

			<Button
				disabled={!changed}
				class=" small"
				on:click={() => {
					set_state(page_name, 'tag', selected.length > 0 ? `${sele}$:${logic}` : '');
					emit('close');
				}}
			>
				<SVG type="check" />
				Ok
			</Button>
		</div>
	</div>
</section>

<style>
	section {
		position: absolute;
		z-index: 1;
		top: 60px;
		left: 0;

		padding: var(--sp3);
		border-radius: var(--sp0);
		background-color: var(--ac5);
		color: var(--ac2);

		border: 2px solid var(--ac3);
	}

	.line {
		display: flex;
		gap: var(--sp1);
		justify-content: space-between;
		align-items: center;
	}
	.input {
		position: relative;
	}

	input {
		padding-right: calc(var(--sp3) * 2);
		width: unset;
	}
	.clear {
		position: absolute;
		top: 0;
		right: var(--sp2);

		display: flex;
		align-items: center;
		height: 100%;
	}

	.tags {
		max-height: 200px;
		overflow-y: auto;
	}
	label {
		display: flex;
		gap: var(--sp2);
		margin-top: var(--sp0);

		font-size: small;
	}
	.hide {
		display: none;
	}

	input[type='checkbox'] {
		width: 20px;
	}
</style>
