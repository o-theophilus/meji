<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Center from '$lib/center.svelte';

	export let page_name;
	let search = '';
	let search_init = '';

	const submit = () => {
		if (search_init != search) {
			search_init = `${search}`;
			set_state(page_name, 'search', search);
		}
	};

	onMount(async () => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
		}
		search_init = `${search}`;
	});
</script>

<div class="search">
	<Center>
		<div class="block">
			<div class="input">
				<div class="float svg">
					<SVG type="search" size="15" />
				</div>

				<input
					class:show_close={search != ''}
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
			<button class="primary" on:click={submit} disabled={search == search_init}>Search</button>
		</div>
	</Center>
</div>

<style>
	.search {
		background-color: var(--ac6);
		padding: var(--sp2) 0;
	}

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
		border: 2px solid var(--ac3);
		border-radius: var(--sp1) 0 0 var(--sp1);
		padding-left: var(--sp5);

		color: var(--ac1);
	}
	input:hover,
	input:focus {
		border-color: var(--cl1);
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
	button:disabled {
		background-color: var(--ac3);
		color: var(--ac4_);
		cursor: unset;
	}
</style>
