<script>
	import { createEventDispatcher } from 'svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	let emit = createEventDispatcher();

	export let page_name = '';
	export let non_default = false;
	export let placeholder = 'Search';
	export let search = '';
	let _search = `${search}`;

	let set = (url) => {
		if (!non_default) {
			_search = search = '';
			if (url.searchParams.has('search')) {
				_search = search = url.searchParams.get('search');
			}
		}
	};

	onMount(() => {
		set($page.url);
	});
	$: set($page.url);

	const submit = (x) => {
		if (x == 'clear' || search.trim() == '') {
			search = '';
		}
		emit(x);

		if (!non_default) {
			if (_search != search) {
				set_state(page_name, 'search', search);
			}
			set($page.url);
		}
	};
</script>

<div class="line">
	<div class="input">
		<div class="float svg">
			<SVG type="search" size="15" />
		</div>

		<input
			class:show_close={search != ''}
			type="text"
			{placeholder}
			bind:value={search}
			on:keypress={(e) => {
				if (e.key == 'Enter') {
					submit('ok');
				}
			}}
		/>

		<div class="float clear">
			{#if search}
				<Button
					class="round"
					on:click={() => {
						submit('clear');
					}}
				>
					<SVG type="close" size="8" />
				</Button>
			{/if}
		</div>
	</div>

	{#if !non_default}
		<Button
			class="primary"
			on:click={() => {
				submit('ok');
			}}
			disabled={search == _search}>Search</Button
		>
	{/if}
</div>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
		width: 100%;
	}

	.input {
		position: relative;

		display: flex;
		align-items: center;
		width: 100%;

		fill: var(--ac3);
	}

	input {
		width: 100%;
		padding: var(--sp1);
		border-radius: var(--sp0);
		padding-left: var(--sp5);
		border: none;

		outline: 2px solid var(--ac4);
		background-color: var(--ac5);
		color: var(--ac1);
	}

	input:hover {
		outline-color: var(--ac3);
	}

	input:focus {
		outline-color: var(--ac1);
	}

	.show_close {
		padding-right: var(--sp5);
	}

	.float {
		position: absolute;
		top: 0;
		display: flex;
		align-items: center;
		height: 100%;
	}

	.clear {
		right: var(--sp1);
	}

	.svg {
		left: var(--sp2);
	}
</style>
