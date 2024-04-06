<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	export let page_name;
	export let order_by;
	export let default_value = '';

	const sort_items = (x) => {
		default_value = x;
		set_state(page_name, 'order', x == 'latest' ? '' : x);
	};

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('order')) {
			default_value = params.get('order');
		}
	});
</script>

<select
	on:change={(e) => {
		sort_items(e.target.value);
	}}
	value={default_value}
>
	{#each order_by as x}
		<option value={x}>
			{x}
		</option>
	{/each}
</select>

<style>
</style>
