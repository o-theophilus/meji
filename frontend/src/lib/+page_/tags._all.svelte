<script>
	// import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { loading, module } from '$lib/store.avelte.js';

	import Form from '$lib/form.svelte';
	import { Tag } from '$lib/button';
	import Input from '$lib/input.svelte';
	import BRound from '$lib/button/round.svelte';
	import Spinner from '$lib/loading_spinner.svelte';

	let tags = [];
	let filter = '';

	// onMount(async () => {
	// 	let i = $state.findIndex((x) => x.name == 'tags');
	// 	if (i != -1) {
	// 		tags = $state[i].data;
	// 	}
	// });

	let loading_tags = true;
	// onMount(async () => {
	// 	let pn = 'tags';
	// 	let i = $state.findIndex((x) => x.name == pn);
	// 	if (i == -1) {
	// 		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
	// 		resp = await resp.json();

	// 		if (resp.status == 200) {
	// 			tags = resp.tags;
	// 			$state.push({
	// 				name: pn,
	// 				data: resp.tags
	// 			});
	// 		}
	// 	} else {
	// 		tags = $state[i].data;
	// 	}
	// 	loading_tags = false;
	// });
</script>

<Form>
	<svelte:fragment slot="title">
		<b>All Tags</b>
	</svelte:fragment>

	<div class="input">
		<Input bind:value={filter} type="text" placeholder="Filter" />
		{#if filter}
			<div class="clear">
				<BRound
					icon="close"
					icon_size="8"
					on:click={() => {
						filter = '';
					}}
				/>
			</div>
		{/if}
	</div>

	<br />

	<div class="tags_space">
		{#if loading_tags}
			<div class="spinner">
				<Spinner active />
			</div>
		{/if}
		{#each tags as tag}
			{#if tag.includes(filter.toLowerCase())}
				<Tag
					on:click={() => {
						// let pn = 'shop';
						// let i = $state.findIndex((x) => x.name == pn);
						// if (i != -1) {
						// 	$state.splice(i, 1);
						// }
						// $state.push({
						// 	name: pn,
						// 	search: `?${new URLSearchParams({ tag }).toString()}`,
						// 	data: [],
						// 	loaded: false
						// });
						// $loading = 'loading . . .';
						// $module = null;
						// goto('/shop');
					}}
				>
					{tag}
				</Tag>
			{/if}
		{/each}
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

	.spinner {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100px;
		width: 100%;
	}
</style>
