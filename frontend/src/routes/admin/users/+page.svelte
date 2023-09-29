<script>
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import User from './user.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Status from './status.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;
	let { page_name } = data;

	let status = ['all', 'confirm', 'anonymous'];
</script>

<Meta title="Users" description="Users" />

<Status {page_name} {status} default_value="all" />

<Card>
	<b> User{users.length > 1 ? 's' : ''} </b>
	<br />
	<br />
	{#each users as x}
		<User user={x} />
	{:else}
		no item here
	{/each}
	<Pagination {page_name} {total_page} />
</Card>

<style>
</style>
