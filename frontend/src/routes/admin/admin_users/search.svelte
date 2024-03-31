<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Search from '$lib/search.svelte';
	import Button from '$lib/button.svelte';

	export let page_name;
	export let permissions;

	let _user = '';
	let _type = 'all';
	let _action = 'all';
	$: search = `${_user || 'all'}:${_type || 'all'}:${_action || 'all'}`;

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			let temp = params.get('search');
			temp = temp.split(':');
			if (temp.length == 3) {
				_user = temp[0] != 'all' ? temp[0] : '';
				_type = temp[1];
				_action = temp[2];
			}
		}
	});
</script>

<section>
	<div class="line">
		<select
			bind:value={_type}
			on:input={() => {
				_action = 'all';
			}}
		>
			{#each Object.entries(permissions) as [type, action]}
				<option value={type}>
					{type}
				</option>
			{/each}
		</select>
		<select bind:value={_action}>
			{#each permissions[_type] as x}
				<option value={x}>
					{x}
				</option>
			{/each}
		</select>
	</div>

	<div class="line">
		<Search
			placeholder="Search for User"
			bind:search={_user}
			on:clear={() => {
				_user = '';
			}}
		/>
		<Button
			class="primary"
			on:click={() => {
				if (search == 'all:all:all') {
					search = '';
				}
				set_state(page_name, 'search', search);
			}}
		>
			Search
		</Button>
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
	}
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
