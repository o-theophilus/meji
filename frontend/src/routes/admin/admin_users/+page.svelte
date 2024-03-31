<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Back from '$lib/button.back.svelte';
	import Meta from '$lib/meta.svelte';
	import User from '../users/user.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Center from '$lib/center.svelte';
	import Search from './search.svelte';
	import Sort from '$lib/sort.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;
	let { permissions } = data;
	let { page_name } = data;

	let sorts = ['latest', 'oldest', 'name (a-z)', 'name (z-a)'];
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
	<Search {page_name} {permissions} />

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
