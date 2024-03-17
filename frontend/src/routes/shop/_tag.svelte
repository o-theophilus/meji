<script>
	import { page } from '$app/stores';
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import Input from '$lib/input.svelte';
	import SVG from '$lib/svg.svelte';

	export let page_name;
	let selected = [];
	let _selected = [];
	let multiply = false;
	let _multiply = false;
	let search = '';

	let tags = [];
	let open_tags = false;

	let selected_string = '';
	let _selected_string = '';
	$: {
		selected_string = selected.sort((a, b) => a - b).join(',');
		selected_string = `${selected_string}${selected.length > 1 && multiply ? ':x' : ''}`;
		_selected_string = _selected.sort((a, b) => a - b).join(',');
		_selected_string = `${_selected_string}${_selected.length > 1 && _multiply ? ':x' : ''}`;
	}

	onMount(async () => {
		let params = $page.url.searchParams;
		if (params.has('tag')) {
			let x = params.get('tag');
			if (x.slice(-2) == ':x') {
				x = x.slice(0, -2);
				multiply = true;
				_multiply = true;
			}
			selected = x.split(',');
			_selected = x.split(',');
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
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
		Tags&nbsp;{#if _selected.length > 0}
			({_selected.length}{#if _multiply}*{/if})
		{/if}

		<span class="angle">
			<SVG type="angle" size="8" />
		</span>
	</Button>

	{#if open_tags}
		<div
			class="container"
			on:click|stopPropagation
			role="presentation"
			transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}
		>
			All Tags

			<br />
			<br />

			<div class="input">
				<Input bind:value={search} type="text" placeholder="Search" />
				{#if search}
					<div class="clear">
						<Button
							class="round"
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
				<label class:disabled={selected.length < 2}>
					<input bind:checked={multiply} type="checkbox" disabled={selected.length < 2} />
					{#if multiply}
						x
					{:else}
						+
					{/if}
				</label>

				<div class="line buttons">
					<Button
						disabled={!_selected_string && !selected_string}
						class="hover_red"
						on:click={() => {
							if (_selected_string) {
								set_state(page_name, 'tag', '');
							}

							open_tags = false;
							selected = [];
							_selected = [];
							multiply = false;
							_multiply = false;
						}}
					>
						<SVG type="close" size="8" />
					</Button>

					<Button
						disabled={_selected_string == selected_string}
						on:click={() => {
							set_state(page_name, 'tag', selected_string);

							open_tags = false;
							_selected = selected;
							_multiply = multiply;
						}}
					>
						<SVG type="check" size="8" />
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

	.container {
		position: absolute;
		z-index: 1;
		top: 40px;
		left: 0;

		padding: var(--sp3);
		border-radius: var(--sp0);
		background-color: var(--ac6);

		outline: 2px solid var(--ac4);
	}

	.input {
		position: relative;
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

	input {
		cursor: pointer;
	}
	input:disabled {
		cursor: default;
	}

	label {
		display: flex;
		gap: var(--sp0);
		margin-top: var(--sp0);
		cursor: pointer;

		font-size: small;
	}

	label:hover {
		color: var(--cl1);
	}

	label.disabled {
		cursor: default;
		color: var(--ac4);
	}

	.hide {
		display: none;
	}

	.line {
		display: flex;
		gap: var(--sp3);
		justify-content: space-between;
		align-items: center;
	}
	.line label {
		text-transform: unset;
	}
	.buttons {
		gap: var(--sp0);
	}
</style>
