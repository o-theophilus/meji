<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Back from '$lib/button.back.svelte';
	import Meta from '$lib/meta.svelte';
	import User from './user.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Status from '$lib/status.svelte';
	import Center from '$lib/center.svelte';
	import Search from '$lib/search.svelte';
	import Sort from '$lib/sort.svelte';
	import SVG from '$lib/svg.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;
	let { page_name } = data;

	let status = ['all', 'confirm', 'anonymous'];
	let sorts = ['latest', 'oldest', 'name (a-z)', 'name (z-a)'];

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
			_search = params.get('search');
		}
	});
</script>

<Meta title="Users" description="Users" />

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			User{users.length > 1 ? 's' : ''}
		</div>
		<div class="line">
			<Sort {page_name} array={sorts} default_value="latest" />
		</div>
	</div>
</Center>

<Card>
	<Status {page_name} array={status} default_value="all" />
	<br />
	<div class="line">
		<Search
			bind:search
			on:ok={() => {
				submit();
			}}
			on:clear={() => {
				search = '';
				submit();
			}}
		/>
		<Button class="primary" on:click={submit} disabled={search == _search}>Search</Button>
	</div>
	<br />
	{#each users as x}
		<User user={x} />
	{:else}
		no item here
	{/each}

	<Pagination {page_name} {total_page} />
</Card>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
