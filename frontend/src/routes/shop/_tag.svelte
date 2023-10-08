<script>
	import { page } from '$app/stores';
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let page_name;
	let selected = [];
	let _selected = [];
	let multiply = false;
	let _multiply = false;
	let search = '';

	let tags = [];
	let open_tags = false;
	let label = '';

	let selected_string = '';
	let _selected_string = '';
	let changed = false;
	$: {
		_selected_string = _selected.sort((a, b) => a - b).join(',');
		selected_string = selected.sort((a, b) => a - b).join(',');
		changed = _selected_string != selected_string || (multiply != _multiply && selected.length > 1);
	}

	onMount(async () => {
		let params = $page.url.searchParams;
		if (params.has('tag')) {
			let x = params.get('tag');
			if (x.slice(-2) == ':x') {
				x = x.slice(0, -2);
				multiply = true;
			}
			selected = x.split(',');
			label = `${selected.length}${multiply ? '*' : ''}`;
		}

		_selected = [...selected];
		_multiply = multiply;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tags`);
		resp = await resp.json();
		if (resp.status == 200) {
			tags = resp.tags;
		}
	});
</script>

<svelte:window
	on:click={() => {
		open_tags = false;
	}}
/>

<div class="tag_position" on:click|stopPropagation role="presentation">
	<Button
		on:click={() => {
			open_tags = !open_tags;
		}}
	>
		Tags {#if label}({label}){/if}
		<span class="angle">
			<SVG type="angle" size="10" />
		</span>
	</Button>

	{#if open_tags}
		<div
			class="tag_block"
			on:click|stopPropagation
			role="presentation"
			transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}
		>
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
							<SVG type="close" size="8" />
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
							open_tags = false;
							if (_selected_string) {
								set_state(page_name, 'tag', '');
							}
							selected = [];
							_selected = [];
							multiply = false;
							label = '';
						}}
					>
						<SVG type="close" />
						<!-- x -->
					</Button>

					<Button
						disabled={!changed}
						class=" small"
						on:click={() => {
							let temp = '';
							if (selected.length > 0) {
								temp = selected_string;
								if (multiply) {
									temp = `${temp}:x`;
								}
							}

							open_tags = false;
							label = `${selected.length}${multiply && selected.length > 0 ? '*' : ''}`;
							set_state(page_name, 'tag', temp);
							_selected = [...selected];
						}}
					>
						<SVG type="check" />
						<!-- Ok -->
					</Button>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.tag_position {
		position: relative;
	}

	.angle {
		transform: rotate(-90deg);
	}

	.tag_block {
		position: absolute;
		z-index: 1;
		top: 40px;
		left: 0;

		padding: var(--sp3);
		border-radius: var(--sp0);
		background-color: var(--ac5);

		outline: 2px solid var(--ac4);
	}

	.line {
		display: flex;
		gap: var(--sp2);
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
		right: var(--sp1);

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
		/* cursor: pointer; */

		font-size: small;
	}

	label:hover {
		/* font-weight: 500; */
		color: var(--cl1);
	}
	.multiply {
		text-transform: lowercase;
	}
	.hide {
		display: none;
	}

	input[type='checkbox'] {
		width: 20px;
		cursor: pointer;
	}
</style>
