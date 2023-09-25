<script>
	import { page } from '$app/stores';
	import { createEventDispatcher, onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	let emit = createEventDispatcher();

	export let tags = [];
	export let page_name;
	let selected = [];
	let multiply = false;
	let search = '';
	let selected_snap = [];
	let multiply_snap;

	$: old = selected_snap.sort((a, b) => a - b).join(',');
	$: new_ = selected.sort((a, b) => a - b).join(',');
	$: changed = old != new_ || (multiply != multiply_snap && selected.length > 1);

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('tag')) {
			let x = params.get('tag');
			if (x.slice(-2) == ':x') {
				x = x.slice(0, -2);
				multiply = true;
			}
			selected = x.split(',');
		}

		selected_snap = [...selected];
		multiply_snap = multiply;
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
		<label class="multiply">
			<input bind:checked={multiply} type="checkbox" />
			{#if multiply}
				x
			{:else}
				+
			{/if}
		</label>

		<div class="line">
			<Button
				disabled={selected.length == 0}
				class="small hover_red"
				on:click={() => {
					selected = [];
					multiply = false;
				}}
			>
				<SVG type="close" />
			</Button>

			<Button
				disabled={!changed}
				class=" small"
				on:click={() => {
					let temp = '';
					if (selected.length > 0) {
						temp = new_;
						if (multiply) {
							temp = `${temp}:x`;
						}
					}
					set_state(page_name, 'tag', temp);
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
		left: -2px;

		padding: var(--sp3);
		border-radius: var(--sp0);
		background-color: var(--ac5);
		color: var(--ac2);

		border-style: none solid solid none;
		border-width: 2px;
		border-color: var(--ac4);
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
	.multiply {
		text-transform: lowercase;
	}
	.hide {
		display: none;
	}

	input[type='checkbox'] {
		width: 20px;
	}
</style>
