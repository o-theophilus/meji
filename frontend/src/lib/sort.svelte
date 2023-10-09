<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	// import SVG from '$lib/svg.svelte';

	export let page_name;
	export let array;
	export let default_value = '';

	const sort_items = (x) => {
		default_value = x;
		set_state(page_name, 'sort', x == 'latest' ? '' : x);
	};

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('sort')) {
			default_value = params.get('sort');
		}
	});
</script>

<select
	on:change={(e) => {
		sort_items(e.target.value);
		// console.log(e.target.value);
	}}
>
	{#each array as x}
		<option value={x}>
			{x}
		</option>
	{/each}
</select>

<style>
</style>
