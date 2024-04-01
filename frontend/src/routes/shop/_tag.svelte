<script>
	import { page } from '$app/stores';

	import { onMount } from 'svelte';
	import { set_state, module } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import Input from '$lib/input.svelte';
	import SVG from '$lib/svg.svelte';
	import Form from '$lib/form.svelte';

	let page_name = $module.page_name;
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

<Form>
	<svelte:fragment slot="title">
		<b class="title">All Tags</b>
		All Tags
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

	<div class="tags">
		{#each tags as x}
			<label class:hide={!x.includes(search.toLowerCase())}>
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
					$module = '';
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
					$module = '';
				}}
			>
				<SVG type="check" size="8" />
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
