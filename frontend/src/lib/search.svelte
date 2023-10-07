<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let page_name;
	export let placeholder = 'Search';
	let search = '';
	let _search = '';

	const submit = () => {
		if (_search != search) {
			_search = `${search}`;
			set_state(page_name, 'search', search);
		}
	};

	onMount(async () => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
		}
		_search = `${search}`;
	});
</script>

<div class="block">
	<div class="slot">
		<slot />
	</div>
	<div class="input">
		<div class="float svg">
			<SVG type="search" size="15" />
		</div>

		<input
			class:show_close={search != ''}
			class:slot={Object.keys($$slots).length > 0}
			type="text"
			{placeholder}
			bind:value={search}
			on:keypress={(e) => {
				if (e.key == 'Enter') {
					submit();
				}
			}}
		/>

		<div class="float clear">
			{#if search}
				<Button
					class="small round"
					on:click={() => {
						search = '';
						submit();
					}}
					disabled={search == _search}
				>
					<SVG type="close" size="8" />
				</Button>
			{/if}
		</div>
	</div>
	<button on:click={submit} disabled={search == _search}>Search</button>
</div>

<style>
	.block {
		display: flex;
	}
	.input {
		position: relative;

		display: flex;
		align-items: center;

		width: 100%;

		fill: var(--ac3);
	}

	.slot {
		flex-shrink: 0;
	}
	input {
		border-radius: var(--sp1) 0 0 var(--sp1);
		padding-left: var(--sp5);
		height: 100%;
	}
	.slot {
		border-radius: 0;
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

	button {
		padding: var(--sp1) var(--sp3);
		border: none;

		border-radius: 0 var(--sp0) var(--sp0) 0;
		background-color: var(--cl1);
		color: var(--ac5_);
		cursor: pointer;
		outline: 2px solid var(--cl1);
	}
	button:hover {
		background-color: var(--cl2);
	}

	button:disabled {
		background-color: var(--ac6);
		outline: 2px solid var(--ac6);
		color: var(--ac4);
		cursor: unset;
	}
</style>
