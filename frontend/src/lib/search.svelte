<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Center from '$lib/center.svelte';

	export let page_name;
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

<!-- <div class="search">
	<Center> -->
		<div class="block">
			<slot />
			<div class="input">
				<div class="float svg">
					<SVG type="search" size="15" />
				</div>

				<input
					class:show_close={search != ''}
					class:slot={Object.keys($$slots).length > 0}
					type="text"
					placeholder="Search"
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
						>
							<SVG type="close" size="15" />
						</Button>
					{/if}
				</div>
			</div>
			<button class="primary" on:click={submit} disabled={search == _search}>Search</button>
		</div>
	<!-- </Center>
</div> -->

<style>
	/* .search {
		background-color: var(--ac6);
		padding: var(--sp2) 0;
	} */

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

	input {
		padding: var(--sp2);
		border: 2px solid var(--ac4);
		border-right: none;
		border-radius: var(--sp1) 0 0 var(--sp1);
		padding-left: var(--sp5);

		color: var(--ac1);
	}
	.slot {
		border-radius: 0;
	}
	input:hover,
	input:focus {
		border-color: var(--ac3);
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
		right: var(--sp2);
	}

	.svg {
		left: var(--sp2);
	}

	button {
		padding: var(--sp2) var(--sp3);
		border: none;
		border-radius: 0 var(--sp1) var(--sp1) 0;
		background-color: var(--cl1);
		color: var(--ac5_);
		cursor: pointer;
	}
	button:hover {
		background-color: var(--cl2);
	}
	button:disabled {
		background-color: var(--ac3);
		color: var(--ac4_);
		cursor: unset;
	}
</style>
