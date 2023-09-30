<script>
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import User from './user.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Status from '$lib/status.svelte';
	import Center from '$lib/center.svelte';
	import Search from '$lib/search.svelte';
	import Sort from '$lib/sort.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;
	let { page_name } = data;

	let status = ['all', 'confirm', 'anonymous'];
	let sorts = ['latest', 'oldest', 'name (a-z)', 'name (z-a)'];
</script>

<Meta title="Users" description="Users" />

<Center>
	<br />
	<div class="title">
		<b> User{users.length > 1 ? 's' : ''} </b>
		<div class="line">
			<Sort {page_name} array={sorts} default_value="latest" />
		</div>
	</div>
</Center>

<Card>
	<Status {page_name} array={status} default_value="all" />
	<br />
	<Search {page_name} />
	<br />
	{#each users as x}
		<User user={x} />
	{:else}
		no item here
	{/each}

	<Pagination {page_name} {total_page} />
</Card>

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--sp2);
		color: var(--ac1);
	}
</style>
