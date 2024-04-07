<script>
	import { page } from '$app/stores';

	import { onMount } from 'svelte';
	import { set_state, module } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import Input from '$lib/input.svelte';
	import SVG from '$lib/svg.svelte';
	import Form from '$lib/form.svelte';
	import Tag from '$lib/button.tag.svelte';

	let tags = [...$module.tags];
	let selected = [];
	let _selected = [];
	let multiply = false;
	let _multiply = false;
	let search = '';

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
	});

	const toggle = (x) => {
		if (selected.includes(x)) {
			selected = selected.filter((i) => i != x);
		} else {
			selected.push(x);
			selected = selected;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b class="title">All Tags</b>
	</svelte:fragment>

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

	<div class="tags_space">
		{#each tags as x}
			<Tag
				hide={!x.includes(search.toLowerCase())}
				active={selected.includes(x)}
				on:click={() => {
					toggle(x);
				}}>{x}</Tag
			>
		{/each}
	</div>

	<br />

	<!-- TODO: check this disables -->
	<div class="line">
		<label class:disabled={selected.length < 2}>
			<input bind:checked={multiply} type="checkbox" disabled={selected.length < 2} />
			{#if multiply}
				all (x)
			{:else}
				any (+)
			{/if}
		</label>

		<div class="line buttons">
			<Button
				disabled={!_selected_string && !selected_string}
				class="hover_red"
				on:click={() => {
					if (_selected_string) {
						set_state($module.page_name, 'tag', '');
					}

					selected = [];
					_selected = [];
					multiply = false;
					_multiply = false;
					$module = '';
				}}
			>
				Clear
			</Button>

			<Button
				disabled={_selected_string == selected_string}
				on:click={() => {
					set_state($module.page_name, 'tag', selected_string);

					_selected = selected;
					_multiply = multiply;
					$module = '';
				}}
			>
				Ok
			</Button>
		</div>
	</div>
</Form>

<style>
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

	.tags_space {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);

		max-height: 200px;
		overflow-y: auto;

		border-radius: var(--sp1);
		padding: var(--sp1);
		border: 2px solid var(--ac4);
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
